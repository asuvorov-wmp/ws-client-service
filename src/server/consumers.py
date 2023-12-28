"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import inspect
import json
import logging
import time

from asgiref.sync import async_to_sync, sync_to_async  # pylint: disable=unused-import

import httpx

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.module_loading import import_string
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError)

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError)

from integrations.epa import EPAClient
from integrations.models import IntegratedAppContext
from integrations.models.choices import AppType
from lib.decorators import log_default
from lib.logger import log, log_dump
from lib.utilities import encoder, models, text

from .epa_constants import (
    EPAEvent,
    UIEventType)
from .epa_state_machine import EPAStateMachine
from .epa_workflow import EPAWorkflow


logger = logging.getLogger(__name__)


class MasterConsumer(AsyncJsonWebsocketConsumer):
    """Master Consumer.

    Since we can only have a single Endpoint per Socket, we need a single Consumer,
    that given the Stream Dispatches to the correct Handler.

    Attributes
    ----------
    epa_sm                  : obj       EPA State Machine Object.
    epa_wf                  : obj       EPA Workflow Object.
    ws_client               : obj       EPA Cloud Client Object.

    hard_reset              : bool      Tells the Consumer, either the App Configuration should be
                                        re-fetched.

    app_context             : obj       App Context Object.
    auth_token              : str       Auth Token.
    app_id                  : str       Application ID.
    device_id               : str       Device ID.

    logging_extra           : dict      Extra logging Parameters.
    stream_handlers         : dict      Stream Handlers.

    Methods
    -------
    __init__()                          Constructor.

    connect()                           Establish Connection.
    disconnect()                        Disconnect.
    receive_json()                      Process Incoming JSON from Client.
    encode_json()                       Encode plain JSON to handle Payloads.
    reply()                             Handler for `lib.channels.send_channel_message`.
    cloud_reply()                       Handler for `lib.channels.send_channel_message`.

    _on_open()                          EPA Cloud on open Connection Handler.
    _on_message()                       EPA Cloud on Message received Handler.
    _on_error()                         EPA Cloud on Error received Handler.
    _on_close()                         EPA Cloud on close Connection Handler.

    """

    epa_sm = EPAStateMachine()
    epa_wf = EPAWorkflow()

    @log_default(my_logger=logger)
    def __init__(self, *args, **kwargs):
        """Create Stream Handlers.

        These used to be multiplexed Consumers.
        """
        super().__init__(*args, **kwargs)

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.hard_reset: bool = False  # Used to let know the Consumer, that the new Connection
                                       # established, and the Configuration needs to be fetched,
                                       # or updated (the Channel Name specifically).

        # --- Client(s).
        self.ws_client: EPAClient = None

        # --- Configuration, based on the Assumption, that one Websocket Connection per one Device
        #     (unique by Device ID and Agent ID).
        self.app_context: IntegratedAppContext = None
        self.auth_token: str = None
        self.app_id: str = None
        self.device_id: str = None

        # --- Miscellaneous.
        self.logging_extra = {}
        self.stream_handlers = {}

        for key, value in settings.WEBSOCKET_STREAM_HANDLERS.items():
            handler = value if not isinstance(value, str) else import_string(value)

            self.stream_handlers[key] = handler(key, self)

    @log_default(my_logger=logger)
    async def connect(self):
        """Establish Connection.

        Since, upon establishing a Webscoket Connection, the Web Client cannot provide either
        Request Headers or Payload with the Data of Interest (e.g. Authentication Token), here we
        simply accept the Connection Request, and handle the Client's Authorization in the
        `self.receive_json()` Method.
        """
        # log(f"[---  DEBUG  ---] SCOPE : \n{encoder.encode(self.scope)}", logger.debug)

        await super().connect()

        log(f"[---  INFO   ---] Channel connected: {self.channel_name}", logger.info)

        # ---------------------------------------------------------------------
        # --- Establish WebSocket Connection with Cloud EPA.
        # ---------------------------------------------------------------------
        try:
            self.ws_client = EPAClient(self)
        except Exception as exc:
            # if self.ws_client:
            #     self.ws_client.disconnect()
            self.close()

            raise exc

        # ---------------------------------------------------------------------
        # --- Accept the Connection and return App UUID and Secret Key.
        # ---------------------------------------------------------------------
        app_integration = await database_sync_to_async(models.get_app)(AppType.INET)

        # ---------------------------------------------------------------------
        # --- Weird "Feature".
        #     Sometimes it gets through, sometimes - throws an Exception.
        # ---------------------------------------------------------------------
        try:
            await self.accept()
        except:
            pass

        await self.reply(dict(
            app_id=app_integration.app_id,
            secret_key=app_integration.secret_key))

        self.hard_reset = True

    @log_default(my_logger=logger)
    async def disconnect(self, code):
        """Disconnect.

        Do Clean-up and ask the Handlers to run their Disconnect.
        """
        super().disconnect(code)

        log(f"Channel disconnected: {self.channel_name}", logger.info)

        for handler in self.stream_handlers.values():
            await handler.perform_disconnect(self.channel_name, code)

        if self.ws_client:
            self.ws_client.disconnect()

        raise StopConsumer

    @log_default(my_logger=logger)
    async def receive_json(self, content: dict, **kwargs):
        """Process Incoming JSON from Client.

        Need to validate the Token, and `perform_receive()` on the appropriate Stream Handler.
        """
        # ---------------------------------------------------------------------
        # --- Initials (verify Request).
        # ---------------------------------------------------------------------
        try:
            (
                self.auth_token,
                self.app_id,
                self.device_id
            ) = self.verify_request(content)
        except NotAuthenticated as exc:
            return await self.reply({
                "stream":           "channel",
                "payload": {
                    "even_type":    UIEventType.ERROR,
                    "message": {
                        "detail":   exc.get_full_details(),
                        "status":   exc.status_code,
                    },
                },
            })
        except ValueError as exc:
            return await self.reply({
                "stream":           "channel",
                "payload": {
                    "even_type":    UIEventType.ERROR,
                    "message": {
                        "detail":   str(exc),
                        "status":   httpx.codes.INTERNAL_SERVER_ERROR,
                    },
                },
            })

        # ---------------------------------------------------------------------
        # --- Manage Command.
        # ---------------------------------------------------------------------
        request_start = time.perf_counter()

        log(f"Channels Request on Channel `{self.channel_name}` with Content {content} started.",
            logger.warning)

        try:
            await self.stream_handlers[content["stream"]].perform_receive(
                content=content,
                reply_channel=self.channel_name)
        except (
                KeyError,
                DecodeError,
                ExpiredSignatureError) as exc:
            log(f"Error authenticating user: {exc}", logger.error)

            await self.reply({
                "stream":           "channel",
                "payload": {
                    "even_type":    UIEventType.ERROR,
                    "message": {
                        "detail":   str(exc),
                        "status":   httpx.codes.INTERNAL_SERVER_ERROR,
                    },
                },
            })
        except (
                AuthenticationFailed,
                NotAuthenticated,
                ValidationError) as exc:
            await self.reply({
                "stream":           "channel",
                "payload": {
                    "even_type":    UIEventType.ERROR,
                    "message": {
                        "detail":   exc.get_full_details(),
                        "status":   exc.status_code,
                    },
                },
            })

        request_stop = time.perf_counter()

        log(f"Channels Request on Channel `{self.channel_name}` with Content {content} "
            f"ended in {request_stop - request_start:.3f} Seconds.",
            logger.warning)

    @classmethod
    async def encode_json(cls, content):
        """Use Django to encode plain JSON to handle our Payloads."""
        return json.dumps(content, cls=DjangoJSONEncoder)

    ###########################################################################
    ###                                                                     ###
    ### CALLBACK FUNCTIONS                                                  ###
    ###                                                                     ###
    ###########################################################################
    @log_default(my_logger=logger)
    async def reply(self, message: dict) -> None:
        """Handler for `lib.channels.send_channel_message`.

        Send the Message (Command) to the Mobile Client.
        """
        # ---------------------------------------------------------------------
        # --- Wedge in the Channel Name, so the Client can log for tracing.
        # ---------------------------------------------------------------------
        message["channel_name"] = self.channel_name

        await self.send_json(message)

    @log_default(my_logger=logger)
    async def cloud_reply(self, message: dict) -> None:
        """Handler for `lib.channels.send_channel_message`.

        Send the Message (Command) to the Cloud EPA.
        """
        self.ws_client.send_message(json.dumps(message["payload"], cls=DjangoJSONEncoder))

    ###########################################################################
    ###                                                                     ###
    ### CALLBACK FUNCTIONS FOR WEBSOCKET CLIENT                             ###
    ###                                                                     ###
    ###########################################################################
    @log_default(my_logger=logger)
    def _on_open(self, wsapp):
        """On open Connection Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.

        """

    @log_default(my_logger=logger)
    def _on_message(self, wsapp, message):
        """On Message received Handler.

        Receive and process the Cloud EPA Event.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        message             : str       Message.

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        message = json.loads(message)
        workstation_device = None

        if not self.app_context:
            self.app_context = models.get_app_context(
                app_id=self.app_id,
                device_id=self.device_id)

        # ---------------------------------------------------------------------
        # --- Fetching the correct Workstation Device.
        #     This can be tricky, because in different Cases, or Situations, we should look at
        #     different associated Device Agents' Parameters or States, in Order to pick up the
        #     right one for the given Moment:
        #     1. If Client is in authenticating Process, Device may not be available or
        #        distinguishable (see below).
        #     2. If Device is in claiming Process, look for `is_connected=False` and
        #        `device_state=EPAState.CLAIMING_PINPAD`.
        #     3. If Device is connected, look for `is_connected=True`.
        # ---------------------------------------------------------------------
        if message.get("ws_connection_identifier", ""):
            workstation_device = models.get_workstation_device(
                device_id=self.device_id,
                is_connected=True,
                raise_exception=False)
            if workstation_device:
                workstation_device.ws_connection_identifier =\
                    message.get("ws_connection_identifier")
                workstation_device.save()

        # ---------------------------------------------------------------------
        # --- Process EPA Event.
        # ---------------------------------------------------------------------
        event = EPAEvent.from_epa_command(message.get("command", ""))
        log_dump({
            "EVENT":    event,
        }, logger=logger.debug)

        self.epa_sm.process_epa_event(
            workstation_device=workstation_device,
            app_context=self.app_context,
            event_type=event,
            epa_message=message)

        async_to_sync(self.reply)(message)

    @log_default(my_logger=logger)
    def _on_error(self, error, *args):
        """On Error received Handler.

        Parameters
        ----------
        error               : str       Error Message.

        """

    @log_default(my_logger=logger)
    def _on_close(self, wsapp, status_code, message):
        """On close Connection Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        status_code         : int       Status Code.
        message             : str       Message.

        """

    ###########################################################################
    ###                                                                     ###
    ### STATIC METHODS                                                      ###
    ###                                                                     ###
    ###########################################################################
    @staticmethod
    def verify_request(content: dict):
        """Verify Request.

        Parameters
        ----------
        content             : dict      Request Content.

        Returns
        -------             : tuple

        Raises
        ------              NotAuthenticated
                            ValueError
        """
        auth_token = content.get("auth_token")
        if not auth_token:
            raise NotAuthenticated("Auth Token is not provided")

        app_id = content.get("app_id")
        device_id = content.get("device_id")
        if not (app_id and device_id):
            raise ValueError("Missing mandatory Parameter(s)")

        return auth_token, app_id, device_id

    ###########################################################################
    ###                                                                     ###
    ### PRIVATE METHODS                                                     ###
    ###                                                                     ###
    ###########################################################################

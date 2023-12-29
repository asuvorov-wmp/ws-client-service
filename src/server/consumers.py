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

from client import CloudService


class MasterConsumer(AsyncJsonWebsocketConsumer):
    """Master Consumer.

    Since we can only have a single Endpoint per Socket, we need a single Consumer,
    that given the Stream Dispatches to the correct Handler.

    Attributes
    ----------
    ws_client               : obj       Cloud Client Object.

    stream_handlers         : dict      Stream Handlers.

    Methods
    -------
    __init__()                          Constructor.

    connect()                           Establish Connection.
    disconnect()                        Disconnect.
    receive_json()                      Process Incoming JSON from Client.
    encode_json()                       Encode plain JSON to handle Payloads.
    reply()                             Handler for `server.channels.send_channel_message`.
    cloud_reply()                       Handler for `server.channels.send_channel_message`.

    """

    def __init__(self, *args, **kwargs):
        """Create Stream Handlers.

        These used to be multiplexed Consumers.
        """
        super().__init__(*args, **kwargs)

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        # --- Client(s).
        self.ws_client: CloudService = None

        # --- Miscellaneous.
        self.stream_handlers = {}

        for key, value in settings.WEBSOCKET_STREAM_HANDLERS.items():
            handler = value if not isinstance(value, str) else import_string(value)

            self.stream_handlers[key] = handler(key, self)

    async def connect(self):
        """Establish Connection."""
        await super().connect()

        # ---------------------------------------------------------------------
        # --- Establish WebSocket Connection with Cloud Service.
        # ---------------------------------------------------------------------
        try:
            self.ws_client = CloudService(self)
        except Exception as exc:
            if self.ws_client:
                self.ws_client.disconnect()

            self.close()

            raise exc

        # ---------------------------------------------------------------------
        # --- Weird "Feature".
        #     Sometimes it gets through, sometimes - throws an Exception.
        # ---------------------------------------------------------------------
        try:
            await self.accept()
        except:
            pass

        await self.reply({
            "status":   "healthy",
        })

    async def disconnect(self, code):
        """Disconnect.

        Do Clean-up and ask the Handlers to run their Disconnect.
        """
        super().disconnect(code)

        for handler in self.stream_handlers.values():
            await handler.perform_disconnect(self.channel_name, code)

        if self.ws_client:
            self.ws_client.disconnect()

        raise StopConsumer

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

        try:
            await self.stream_handlers[content["stream"]].perform_receive(
                content=content,
                reply_channel=self.channel_name)
        except (
                KeyError,
                DecodeError,
                ExpiredSignatureError) as exc:

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

    @classmethod
    async def encode_json(cls, content):
        """Use Django to encode plain JSON to handle our Payloads."""
        return json.dumps(content, cls=DjangoJSONEncoder)

    ###########################################################################
    ###                                                                     ###
    ### CALLBACK FUNCTIONS                                                  ###
    ###                                                                     ###
    ###########################################################################
    async def reply(self, message: dict) -> None:
        """Handler for `lib.channels.send_channel_message`.

        Send the Message (Command) to the Mobile Client.
        """
        # ---------------------------------------------------------------------
        # --- Wedge in the Channel Name, so the Client can log for tracing.
        # ---------------------------------------------------------------------
        message["channel_name"] = self.channel_name

        await self.send_json(message)

    async def cloud_reply(self, message: dict) -> None:
        """Handler for `lib.channels.send_channel_message`.

        Send the Message (Command) to the Cloud EPA.
        """
        self.ws_client.send_message(json.dumps(message["payload"], cls=DjangoJSONEncoder))

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

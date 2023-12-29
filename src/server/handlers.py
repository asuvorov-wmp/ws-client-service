"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

from asgiref.sync import async_to_sync, sync_to_async


class WebsocketStreamHandler:
    """Base Class to handle Websocket Streams.

    Methods
    -------
    __init__()                          Constructor.

    perform_receive()                   Process received Message.
    perform_disconnect()                Process disconnect.
    send()                              Send Message.

    """

    def __init__(self, stream, consumer) -> None:
        """Constructor.

        Parameters
        ----------
        stream              : str       Stream Name.
        consumer            : obj       Consumer Object.

        """
        super().__init__()

        self.stream = stream
        self.consumer = consumer

    async def perform_receive(self, content: dict, reply_channel: str=None, **kwargs) -> None:
        """Almost always overridden.

        Parameters
        ----------
        content             : dict      Message Content.
        reply_channel       : str       Reply Channel Name.

        """

    async def perform_disconnect(self, reply_channel: str=None, code: str=None, **kwargs) -> None:
        """Override, if need to do something on Websocket Close.

        Parameters
        ----------
        reply_channel       : str       Reply Channel Name.
        code                : str       Exit Code.

        """

    async def send(self, message: dict) -> None:
        """Chuck Stream into the Message, so the Client can multiplex.

        Parameters
        ----------
        message             : dict      Message to send.

        """
        await self.consumer.reply({
            "stream":   self.stream,
            "payload":  message,
        })


class PingStreamHandler(WebsocketStreamHandler):
    """Ping Stream Handler."""

    async def perform_receive(self, content: dict, reply_channel: str=None, **kwargs) -> None:
        """Ping simply responds like a Heartbeat.

        Parameters
        ----------
        content             : dict      Message Content.
        reply_channel       : str       Reply Channel Name.

        """
        await self.send({
            "status":   "healthy",
        })


class ChannelStreamHandler(WebsocketStreamHandler):
    """Channel Stream Handler.

    Methods
    -------
    __init__()                          Constructor.

    perform_receive()                   Process received JSON from Client.
    perform_disconnect()                Process Disconnection.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Constructor."""
        super().__init__( *args, **kwargs)

    async def perform_receive(self, content: dict, reply_channel: str=None, **kwargs) -> None:
        """Ping simply responds like a Heartbeat.

        Parameters
        ----------
        content             : dict      Message Content.
        reply_channel       : str       Reply Channel Name.

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Manage Command.
        # ---------------------------------------------------------------------
        if content["command"] == EPACommand.AUTHENTICATE:
            # -----------------------------------------------------------------
            # --- Authenticate Caller against Cloud EPA.
            app_context = await sync_to_async(models.create_update_app_context)(
                auth_token=self.consumer.auth_token,
                app_id=self.consumer.app_id,
                device_id=self.consumer.device_id,
                reply_channel=reply_channel)

            await sync_to_async(self.epa_wf.authenticate)(
                app_context=app_context)

        elif content["command"] == EPACommand.APP_VERSION_REQUEST:
            # -----------------------------------------------------------------
            # --- Request App Version Details from Cloud EPA.
            workstation_device = await sync_to_async(models.get_workstation_device)(
                device_id=self.consumer.device_id,
                is_connected=True)

            await sync_to_async(self.epa_wf.app_version_requested)(
                workstation_device=workstation_device)

        elif content["command"] == EPACommand.DEVICE_CLAIM:
            # -----------------------------------------------------------------
            # --- Claim Pinpad against Cloud EPA.
            workstation_device = await sync_to_async(models.get_workstation_device)(
                device_id=self.consumer.device_id,
                device_agent_id=content.get("device_agent_id"))

            await sync_to_async(self.epa_wf.claim_pinpad)(
                workstation_device=workstation_device,
                input_data=content)

        elif content["command"] == EPACommand.DEVICE_RELEASE:
            # -----------------------------------------------------------------
            # --- Release Pinpad against Cloud EPA.
            workstation_device = await sync_to_async(models.get_workstation_device)(
                device_id=self.consumer.device_id,
                is_connected=True)

            await sync_to_async(self.epa_wf.release_pinpad)(workstation_device)

        elif content["command"] == EPACommand.TRANSACTION_REQUEST:
            # -----------------------------------------------------------------
            # --- Initiate Transaction against Cloud EPA.
            await sync_to_async(self.epa_sm.process_cloud_transaction)(
                workstation_device=workstation_device,
                input_data=content,
                command=content["command"],
                trx_type=content["transaction_type"],
                send_command=True)

        elif content["command"] == EPACommand.TRANSACTION_ABORT:
            # -----------------------------------------------------------------
            # --- Abort Transaction against Cloud EPA.
            await sync_to_async(self.epa_sm.process_cloud_transaction)(
                workstation_device=workstation_device,
                command=content["command"],
                send_command=True)

    async def perform_disconnect(self, reply_channel: str=None, code: str=None, **kwargs) -> None:
        """Override, if need to do something on Websocket Close.

        Parameters
        ----------
        reply_channel       : str       Reply Channel Name.
        code                : str       Exit Code.

        """

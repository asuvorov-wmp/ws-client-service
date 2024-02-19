from asgiref.sync import async_to_sync, sync_to_async

from django.conf import settings

from .channels import send_channel_message


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
        """Parse and manage the Content (Message)."""
        if content["command"] == "some_command":
            pass  # Do Something.
        elif content["command"] == "another_command":
            pass  # Do Something.

        await self.send(content)
        send_channel_message(
            stream=settings.VALID_STREAM_NAMES["CHANNEL"],
            reply_channel=reply_channel,
            payload=content,
            invokee="cloud.reply")

    async def perform_disconnect(self, reply_channel: str=None, code: str=None, **kwargs) -> None:
        """Override, if need to do something on Websocket Close.

        Parameters
        ----------
        reply_channel       : str       Reply Channel Name.
        code                : str       Exit Code.

        """

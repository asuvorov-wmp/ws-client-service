import _thread
import json
import logging

import websocket

from asgiref.sync import async_to_sync, sync_to_async  # pylint: disable=unused-import
from django.conf import settings


logger = logging.getLogger(__name__)


class CloudService:
    """Cloud Service Client Interface."""

    BASE_API_URL = f"{settings.CLOUD_SERVICE_INSTANCE}/"  # Base URL.

    def __init__(self, consumer=None):
        """Constructor."""
        super().__init__()

        self.consumer = consumer  # Websocket Consumer Object.
        self.ws_client = None     # Cloud Client Object.

        self.connect()

    def connect(self):
        """Connect to WebSocket."""
        _thread.start_new_thread(self.__connect, (self.BASE_API_URL,))

    def disconnect(self):
        """Disconnect from WebSocket."""
        self.ws_client.close()

    def send_message(self, message: str):
        """Send the Message."""
        self.ws_client.send(message)

    ###########################################################################
    ###                                                                     ###
    ### CALLBACK FUNCTIONS FOR WEBSOCKET CLIENT                             ###
    ###                                                                     ###
    ###########################################################################
    def __connect(self, url: str):
        """Connect to WebSocket."""
        websocket.enableTrace(True)

        self.ws_client = websocket.WebSocketApp(
            url,
            on_ping=self.__on_ping,
            on_pong=self.__on_pong,
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close)
        self.ws_client.run_forever()

    def __on_ping(self, wsapp, message: str):
        """On Ping Handler."""

    def __on_pong(self, wsapp, message: str):
        """On Pong Handler."""

    def __on_open(self, wsapp):
        """On open Connection Handler."""
        # self.ws_client.send("{}")

    def __on_message(self, wsapp, message: str):
        """On Message received Handler."""
        message = json.loads(message)

        self.sm.process_cloud_event(message)

        async_to_sync(self.consumer.reply)(message)

    def __on_error(self, error: str, *args):
        """On Error received Handler."""

    def __on_close(self, wsapp, status_code: int, message: str):
        """On close Connection Handler."""

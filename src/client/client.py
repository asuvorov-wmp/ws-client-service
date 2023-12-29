import _thread
import json
import logging

import websocket

from asgiref.sync import async_to_sync, sync_to_async  # pylint: disable=unused-import
from django.conf import settings


logger = logging.getLogger(__name__)


class CloudService:
    """Cloud Service Client Interface.

    Attributes
    ----------
    BASE_API_URL            : str       Base URL.
    HEADERS                 : dict      Request Headers.

    ws_client               : obj       Cloud Client Object.

    Methods
    -------
    __init__()                          Constructor.

    connect()                           Connect to WebSocket.
    disconnect()                        Disconnect from WebSocket.
    send_message()                      Send the Message.

    __connect()                         Connect to WebSocket.
    __on_ping()                         On Ping Handler.
    __on_pong()                         On Pong Handler.
    __on_open()                         On open Connection Handler.
    __on_message()                      On Message received Handler.
    __on_error()                        On Error received Handler.
    __on_close()                        On close Connection Handler.

    """

    BASE_API_URL = f"{settings.EPA_CLOUD_INSTANCE}/"
    HEADERS = {
        "Accept-Language":  "en",
        "Content-Type":     "application/json",
    }

    def __init__(self, consumer=None):
        """Constructor.

        Parameters
        ----------
        consumer            : obj       Consumer Object.

        """
        super().__init__()

        self.consumer = consumer
        self.ws_client = None
        self.connect()

    def connect(self):
        """Connect to WebSocket."""
        # self.__connect(self.BASE_API_URL)

        _thread.start_new_thread(self.__connect, (self.BASE_API_URL,))

    def disconnect(self):
        """Disconnect from WebSocket."""
        self.ws_client.close()

    def send_message(self, message):
        """Send the Message.

        Parameters
        ----------
        message             : str       Message.

        """
        self.ws_client.send(message)

    ###########################################################################
    ###                                                                     ###
    ### CALLBACK FUNCTIONS FOR WEBSOCKET CLIENT                             ###
    ###                                                                     ###
    ###########################################################################
    def __connect(self, url):
        """Connect to WebSocket.

        Parameters
        ----------
        url                 : str       WebSocket URL.

        """
        # ---------------------------------------------------------------------
        # --- WebSocketApp Example is best for a long-lived Connection.
        # ---------------------------------------------------------------------
        # websocket.enableTrace(True)

        self.ws_client = websocket.WebSocketApp(
            url,
            on_ping=self.__on_ping,
            on_pong=self.__on_pong,
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close)

        # ---------------------------------------------------------------------
        # --- Set Dispatcher to automatic reconnecting.
        #     3 Second reconnect Delay, if Connection dropped unexpectedly.
        # ---------------------------------------------------------------------
        self.ws_client.run_forever()
        # self.ws_client.run_forever(
        #     dispatcher=rel,
        #     reconnect=3)
        # rel.signal(2, rel.abort)  # Keyboard Interrupt.
        # rel.dispatch()

    def __on_ping(self, wsapp, message):
        """On Ping Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        message             : str       Message.

        """

    def __on_pong(self, wsapp, message):
        """On Pong Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        message             : str       Message.

        """

    def __on_open(self, wsapp):
        """On open Connection Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.

        """
        # self.ws_client.send("{}")

    def __on_message(self, wsapp, message):
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

        # ---------------------------------------------------------------------
        # --- Process Cloud Event.
        # ---------------------------------------------------------------------
        self.sm.process_cloud_event(message)

        async_to_sync(self.consumer.reply)(message)

    def __on_error(self, error, *args):
        """On Error received Handler.

        Parameters
        ----------
        error               : str       Error Message.

        """

    def __on_close(self, wsapp, status_code, message):
        """On close Connection Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        status_code         : int       Status Code.
        message             : str       Message.

        """

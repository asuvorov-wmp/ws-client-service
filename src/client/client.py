"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import _thread
import logging

import websocket

from django.conf import settings

from lib.decorators import log_default


logger = logging.getLogger(__name__)


class EPAClient:
    """Cloud EPA Client Interface.

    Attributes
    ----------
    BASE_API_URL            : str       Base URL.
    HEADERS                 : dict      Request Headers.

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

    @log_default(my_logger=logger)
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

    @log_default(my_logger=logger)
    def send_message(self, message):
        """Send the Message.

        Parameters
        ----------
        message             : str       Message.

        """
        self.ws_client.send(message)

    @log_default(my_logger=logger)
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
            # on_ping=self.__on_ping,
            # on_pong=self.__on_pong,
            on_open=self.consumer._on_open if self.consumer else self.__on_open,
            on_message=self.consumer._on_message if self.consumer else self.__on_message,
            on_error=self.consumer._on_error if self.consumer else self.__on_error,
            on_close=self.consumer._on_close if self.consumer else self.__on_close)

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

    @log_default(my_logger=logger)
    def __on_ping(self, wsapp, message):
        """On Ping Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        message             : str       Message.

        """

    @log_default(my_logger=logger)
    def __on_pong(self, wsapp, message):
        """On Pong Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        message             : str       Message.

        """

    @log_default(my_logger=logger)
    def __on_open(self, wsapp):
        """On open Connection Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.

        """
        # self.ws_client.send("{}")

    @log_default(my_logger=logger)
    def __on_message(self, wsapp, message):
        """On Message received Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        message             : str       Message.

        """

    @log_default(my_logger=logger)
    def __on_error(self, error, *args):
        """On Error received Handler.

        Parameters
        ----------
        error               : str       Error Message.

        """

    @log_default(my_logger=logger)
    def __on_close(self, wsapp, status_code, message):
        """On close Connection Handler.

        Parameters
        ----------
        wsapp               : obj       WebSocket Client Object.
        status_code         : int       Status Code.
        message             : str       Message.

        """

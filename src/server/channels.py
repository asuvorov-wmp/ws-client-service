"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import json

from django.core.serializers.json import DjangoJSONEncoder

from asgiref.sync import async_to_sync
from channels.layers import (
    channel_layers,
    DEFAULT_CHANNEL_LAYER)
from django.conf import settings

from . import encoder


def log_channel_message(message: str, stream: str, reply_channel: str, payload: dict) -> None:
    """Log Channel Message to Console.

    Parameters
    ----------
    message                 : str       Message.
    stream                  : str       Name of Channel to send to.
    reply_channel           : str       Reply Channel to use for sending Message.
    payload                 : dict      Payload of the Message to send.

    """
    print(
        f"`{message}` on `{reply_channel}` -> Stream=`{stream}` -> Message:"
        f"\n{encoder.encode(payload)}")


def send_channel_message(
        stream: str=settings.VALID_STREAM_NAMES["CHANNEL"],
        reply_channel: str,
        payload: dict,
        invokee: str="reply") -> None:
    """Send a Message for a given Channel/Stream.

    Parameters
    ----------
    stream                  : str       Name of Channel to send to.
    reply_channel           : str       Reply Channel to use for sending Message.
    payload                 : dict      Payload of the Message to send.
    invokee                 : str       Name of the Method, that should be invoked on Consumer,
                                        that receives the Event.
    """
    log_channel_message(
        message="Channel Message",
        stream=stream,
        reply_channel=reply_channel,
        payload=payload)

    channel_layer = channel_layers[DEFAULT_CHANNEL_LAYER]
    p = json.loads(json.dumps(payload, cls=DjangoJSONEncoder))

    try:
        async_to_sync(channel_layer.send)(reply_channel, {
            "type":     invokee,
            "stream":   stream,
            "payload":  p,
        })
    except TypeError:
        pass

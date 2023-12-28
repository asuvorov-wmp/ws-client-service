"""
(C) 1995-2022 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

from uvicorn.workers import UvicornWorker

try:
    import os
    import uvloop

    class Worker(UvicornWorker):
        """
        In order to run under `gunicorn`, we want to be able to force `uvloop`, and configure
        `ws_ping`, if needed.

        NOTE: We'd call `gunicorn` as:

        gunicorn asgi:channel_layer --worker-class uvicorn_worker.Worker --reload
        gunicorn asgi:channel_layer
            --workers {{ ansible_facts['ansible_processor_cores'] }} \
            --forwarded-allow-ips '*'
            --worker-class uvicorn_worker.Worker \
            --bind unix:/opt/toogo/run/r1.2.3.4.ws
        """

        ws_ping_interval = float(os.environ.get("WS_PING_INTERVAL", 20.0))
        ws_ping_timeout = float(os.environ.get("WS_PING_TIMEOUT", 20.0))

        CONFIG_KWARGS = {
            "loop":             "uvloop",
            "http":             "auto",
            "proxy_headers":    True,
            "ws_ping_interval": ws_ping_interval,
            "ws_ping_timeout":  ws_ping_timeout,
            "use_colors":       True,
        }

except ImportError:
    Worker = UvicornWorker

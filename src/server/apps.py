from importlib import import_module

from django.apps import AppConfig


class ServerConfig(AppConfig):
    """Docstring."""

    name = "server"
    verbose_name = "Server"

    def ready(self):
        """Docstring."""
        import_module("server.tasks")

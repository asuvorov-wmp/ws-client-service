from importlib import import_module

from django.apps import AppConfig


class ClientConfig(AppConfig):
    """Docstring."""

    name = "client"
    verbose_name = "Client"

    def ready(self):
        """Docstring."""
        import_module("client.tasks")

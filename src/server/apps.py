"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

from importlib import import_module

from django.apps import AppConfig


class ServiceConfig(AppConfig):
    """Docstring."""

    name = "service"
    verbose_name = "Service"

    def ready(self):
        """Docstring."""
        import_module("service.tasks")

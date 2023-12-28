"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import os
import django

from channels.routing import get_default_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

django.setup()


channel_layer = get_default_application()

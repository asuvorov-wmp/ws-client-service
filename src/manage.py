"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

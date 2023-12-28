"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import os
import sys

from django.core.wsgi import get_wsgi_application


project_dir = os.path.dirname(__file__)

sys.path.append(project_dir)
sys.path.append(os.path.join(project_dir, "epa"))

application = get_wsgi_application()

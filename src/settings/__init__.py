"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import django

from django.utils.encoding import force_str
from django.utils.encoding import smart_str
from django.utils.translation import gettext, gettext_lazy


django.utils.encoding.force_text = force_str
django.utils.encoding.smart_text = smart_str
django.utils.encoding.smart_unicode = smart_str
django.utils.translation.ugettext = gettext
django.utils.translation.ugettext_lazy = gettext_lazy

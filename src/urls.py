"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    include,
    re_path)


admin.autodiscover()


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

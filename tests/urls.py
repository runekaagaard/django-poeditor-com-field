# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from poeditor_com_field.urls import urlpatterns as poeditor_com_field_urls

urlpatterns = [
    url(r'^', include(poeditor_com_field_urls, namespace='poeditor_com_field')),
]

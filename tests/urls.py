# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django.urls import path

from .views import test_user, test_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", test_view, name="test"),
    path("user", test_user, name="user"),
]

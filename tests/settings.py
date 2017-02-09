# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "poeditor_com_field",
    "tests"
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

CELERY_ALWAYS_EAGER = True

POEDITOR_API_TOKEN = os.environ['TEST_POEDITOR_API_TOKEN']
POEDITOR_PROJECT_ID = os.environ['TEST_POEDITOR_PROJECT_ID']
POEDITOR_CONTEXT = 'FieldInDatabase'

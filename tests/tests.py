#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from poeditor_com_field.models import Link
from poeditor_com_field.core import sync_existing_models, retry_sync_links
from .models import TestModel


class TestPackage(TestCase):
    """
    def test_no_duplicates(self):
        x = TestModel.objects.create(title="title1")

        x.title = 'woot'
        x.save()

        z = TestModel.objects.create(title="woot")

        y = TestModel.objects.create(title="nihimu")
        y.delete()

        x.delete()
        z.delete()
    """

    def test_sync_existing_models(self):
        TestModel.objects.create(title="niels")
        x = TestModel.objects.create(title="poul")
        x.title = "niels"
        x.save()
        Link.objects.all().update(in_sync_with_server=False)
        print "HEREHEREHERE"
        retry_sync_links()

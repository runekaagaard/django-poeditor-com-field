#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from poeditor_com_field.models import *
from poeditor_com_field.fields import *
from .models import TestModel
    

class TestPackage(TestCase):
    def test_no_duplicates(self):
        x = TestModel.objects.create(title="title1")

        x.title = 'woot'
        x.save()

        TestModel.objects.create(title="woot")

        y = TestModel.objects.create(title="nihimu")
        y.delete()

        for link in Link.objects.all():
            print link

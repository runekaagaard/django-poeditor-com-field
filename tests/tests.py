#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from poeditor_com_field.models import *
from poeditor_com_field.fields import *
from .models import TestModel
    

class TestPoeditor_com_field(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_no_duplicates(self):
        TestModel.objects.create(title="title1")
        obj = TestModel.objects.create(title="title2")
        self.assertEqual(Link.objects.count(), 2)
        obj.title = "title3"
        obj.save()
        for link in Link.objects.all():
            print link
        self.assertEqual(Link.objects.count(), 2)

    def test_links_are_marked_as_posted(self):
        TestModel.objects.create(title="title1")
        self.assertTrue(Link.objects.get(pk=1).posted)

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
    
    def test_something(self):
        obj = TestModel(title="title1")
        obj.save()
        self.assertEqual(obj.pk, 1)

        obj.title = "title2"
        obj.save()

        TestModel.objects.create(title="title2")

        for term in Term.objects.all():
            print term

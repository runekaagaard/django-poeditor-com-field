#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from poeditor_com_field.models import *


class TestPoeditor_com_field(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_something(self):
        bloom_filter, _ = BloomFilter.objects.get_or_create(key='existing_terms')
        

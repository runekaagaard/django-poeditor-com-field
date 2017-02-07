# -*- coding: utf-8 -*-

from django.db import models


class BloomFilter(models.Model):
    key = models.TextField('Key')
    data = models.TextField('Data')

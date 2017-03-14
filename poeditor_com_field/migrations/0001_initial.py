# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(unique=True, max_length=40, db_index=True)),
                ('count', models.IntegerField(default=0)),
                ('exists_on_server', models.BooleanField(default=False)),
                ('in_sync_with_server', models.BooleanField(default=False)),
                ('references', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

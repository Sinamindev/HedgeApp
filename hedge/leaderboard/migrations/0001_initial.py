# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leaders',
            fields=[
                ('username', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('add_date', models.DateTimeField(verbose_name='Date added')),
            ],
        ),
    ]

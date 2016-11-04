# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('symbol', models.CharField(max_length=20)),
                ('market', models.CharField(max_length=80)),
                ('company_name', models.CharField(max_length=100)),
            ],
        ),
    ]

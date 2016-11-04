# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20151002_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='company',
            field=models.CharField(default='Name not available', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='owned',
            name='symbol',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='symbol',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='symbol',
            field=models.CharField(max_length=12),
        ),
    ]

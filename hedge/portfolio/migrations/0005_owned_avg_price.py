# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_auto_20151102_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='owned',
            name='avg_price',
            field=models.DecimalField(max_digits=20, default=0.0, decimal_places=2),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0003_auto_20151102_2028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='valuation',
            old_name='today_valuation',
            new_name='day_valuation',
        ),
        migrations.AddField(
            model_name='valuation',
            name='current_valuation',
            field=models.DecimalField(max_digits=20, default=1000000.0, decimal_places=2),
            preserve_default=False,
        ),
    ]

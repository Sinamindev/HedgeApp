# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='purchase_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='transactions',
            old_name='purchase_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='sell_date',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='sell_price',
        ),
        migrations.AddField(
            model_name='transactions',
            name='buy',
            field=models.BooleanField(default=datetime.datetime(2015, 10, 2, 23, 50, 0, 761659, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

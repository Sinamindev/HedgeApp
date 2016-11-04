# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stock_industry'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stock',
        ),
    ]

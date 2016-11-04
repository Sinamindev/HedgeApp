# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20151025_1337'),
        ('leaderboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valuations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('today_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('week_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('month_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('year_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('user', models.ForeignKey(to='portfolio.Portfolio')),
            ],
        ),
        migrations.DeleteModel(
            name='Leaders',
        ),
    ]

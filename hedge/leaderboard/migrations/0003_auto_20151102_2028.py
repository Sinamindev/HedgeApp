# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_auto_20151102_2028'),
        ('leaderboard', '0002_auto_20151030_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valuation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('today_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('week_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('month_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('year_valuation', models.DecimalField(max_digits=20, decimal_places=2)),
                ('user', models.ForeignKey(to='portfolio.Portfolio')),
            ],
        ),
        migrations.RemoveField(
            model_name='valuations',
            name='user',
        ),
        migrations.DeleteModel(
            name='Valuations',
        ),
    ]

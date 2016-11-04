# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owned',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('symbol', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('purchase_date', models.DateTimeField(verbose_name='Date purchased')),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('username', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('money', models.DecimalField(decimal_places=2, max_digits=12)),
                ('add_date', models.DateTimeField(verbose_name='Date added')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('symbol', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('purchase_date', models.DateTimeField(verbose_name='Date added')),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('sell_date', models.DateTimeField(verbose_name='Date added')),
                ('user', models.ForeignKey(to='portfolio.Portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('symbol', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to='portfolio.Portfolio')),
            ],
        ),
        migrations.AddField(
            model_name='owned',
            name='user',
            field=models.ForeignKey(to='portfolio.Portfolio'),
        ),
    ]

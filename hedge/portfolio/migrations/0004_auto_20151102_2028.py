# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20151025_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('symbol', models.CharField(max_length=8)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('date', models.DateTimeField(verbose_name='Date added')),
                ('buy', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='user',
        ),
        migrations.RemoveField(
            model_name='owned',
            name='purchase_date',
        ),
        migrations.RemoveField(
            model_name='owned',
            name='purchase_price',
        ),
        migrations.AlterField(
            model_name='owned',
            name='symbol',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='money',
            field=models.DecimalField(max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='username',
            field=models.CharField(max_length=80, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='symbol',
            field=models.CharField(max_length=8),
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(to='portfolio.Portfolio'),
        ),
    ]

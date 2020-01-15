# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-07 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(max_length=50, verbose_name='玩家名称')),
                ('score', models.IntegerField(default=0, verbose_name='分数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
            ],
            options={
                'db_table': 'scorelist',
            },
        ),
    ]

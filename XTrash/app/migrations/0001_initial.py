# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-11 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoName', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('createdDateTime', models.DateTimeField(verbose_name='created date')),
                ('analysispath', models.CharField(max_length=100)),
            ],
        ),
    ]

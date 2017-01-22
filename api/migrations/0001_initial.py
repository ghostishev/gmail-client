# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-22 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('snippet', models.CharField(max_length=255)),
            ],
        ),
    ]
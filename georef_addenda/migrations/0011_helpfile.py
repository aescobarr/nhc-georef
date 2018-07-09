# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-04 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import georef.tasks


class Migration(migrations.Migration):

    dependencies = [
        ('georef_addenda', '0010_auto_20180315_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpFile',
            fields=[
                ('id', models.CharField(default=georef.tasks.pkgen, max_length=200, primary_key=True, serialize=False)),
                ('titol', models.TextField()),
                ('file', models.FileField(upload_to='helpfile_uploads')),
            ],
        ),
    ]
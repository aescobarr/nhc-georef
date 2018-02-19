# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-14 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('georef_addenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geometriatoponimversio',
            name='idversio',
            field=models.ForeignKey(blank=True, db_column='idversio', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='geometries', to='georef.Toponimversio'),
        ),
    ]

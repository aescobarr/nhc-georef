# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-11-16 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('georef_addenda', '0016_auto_20191113_1524'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'verbose_name': 'Autor'},
        ),
        migrations.AlterModelOptions(
            name='geometriarecurs',
            options={'verbose_name': 'Geometria de recurs de georeferenciació'},
        ),
        migrations.AlterModelOptions(
            name='geometriatoponimversio',
            options={'verbose_name': 'Geometria de versió de topònim'},
        ),
        migrations.AlterModelOptions(
            name='helpfile',
            options={'verbose_name': "Fitxer d'ajuda"},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Organització'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': "Perfil d'usuari"},
        ),
    ]
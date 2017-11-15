# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Ambitexclosrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idambitgeografic = models.ForeignKey('Ambitgeografic', models.DO_NOTHING, db_column='idambitgeografic')
    idrecursgeoref = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecursgeoref')

    class Meta:
        managed = False
        db_table = 'ambitexclosrecursgeoref'
        unique_together = (('id', 'id'), ('idambitgeografic', 'idrecursgeoref'),)


class Ambitgeografic(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)
    codi = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ambitgeografic'
        unique_together = (('id', 'id'),)


class Ambitgeograficrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idambitgeografic = models.ForeignKey(Ambitgeografic, models.DO_NOTHING, db_column='idambitgeografic')
    idrecursgeoref = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecursgeoref')

    class Meta:
        managed = False
        db_table = 'ambitgeograficrecursgeoref'
        unique_together = (('idambitgeografic', 'idrecursgeoref'), ('id', 'id'),)


class Autorrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idrecursgeoref = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecursgeoref')
    idpersona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='idpersona')

    class Meta:
        managed = False
        db_table = 'autorrecursgeoref'
        unique_together = (('idpersona', 'idrecursgeoref'), ('id', 'id'),)


class Conversio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'conversio'
        unique_together = (('id', 'id'),)


class Recursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=500)
    comentarisnoambit = models.CharField(max_length=500, blank=True, null=True)
    toponim = models.CharField(max_length=500, blank=True, null=True)
    idprojeccio = models.CharField(max_length=500, blank=True, null=True)
    iddatum = models.CharField(max_length=500, blank=True, null=True)
    idunitath = models.CharField(max_length=500, blank=True, null=True)
    idunitatv = models.CharField(max_length=500, blank=True, null=True)
    versio = models.CharField(max_length=100, blank=True, null=True)
    fitxergraficbase = models.CharField(max_length=100, blank=True, null=True)
    idconversio = models.CharField(max_length=100, blank=True, null=True)
    idsuport = models.ForeignKey('Suport', models.DO_NOTHING, db_column='idsuport', blank=True, null=True)
    urlsuport = models.CharField(max_length=250, blank=True, null=True)
    ubicaciorecurs = models.CharField(max_length=200, blank=True, null=True)
    actualitzaciosuport = models.CharField(max_length=250, blank=True, null=True)
    mapa = models.CharField(max_length=100, blank=True, null=True)
    comentariinfo = models.TextField(blank=True, null=True)
    comentariconsulta = models.TextField(blank=True, null=True)
    comentariqualitat = models.TextField(blank=True, null=True)
    classificacio = models.CharField(max_length=300, blank=True, null=True)
    divisiopoliticoadministrativa = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recursgeoref'
        unique_together = (('id', 'id'),)

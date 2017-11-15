# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Comarques(models.Model):
    idcomarca = models.ForeignKey('Objectessipan', models.DO_NOTHING, db_column='idcomarca', primary_key=True)
    codicomarca = models.CharField(max_length=100, blank=True, null=True)
    nomcomarca = models.CharField(max_length=255)
    areaoficial = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    areareal = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    iddemarcacioterritorial = models.ForeignKey('Demarcacionsterritorials', models.DO_NOTHING, db_column='iddemarcacioterritorial', blank=True, null=True)
    idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comarques'


class Comarquesprovincies(models.Model):
    idcomarca = models.ForeignKey(Comarques, models.DO_NOTHING, db_column='idcomarca', primary_key=True)
    idprovincia = models.ForeignKey('Provincies', models.DO_NOTHING, db_column='idprovincia')

    class Meta:
        managed = False
        db_table = 'comarquesprovincies'
        unique_together = (('idcomarca', 'idprovincia'),)


class Comunitatsautonomes(models.Model):
    id = models.ForeignKey('Objectessipan', models.DO_NOTHING, db_column='id', primary_key=True)
    nomcomunitatautonoma = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'comunitatsautonomes'


class Comunitatsautonomesprovincies(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idcomunitatautonoma = models.ForeignKey(Comunitatsautonomes, models.DO_NOTHING, db_column='idcomunitatautonoma')
    idprovincia = models.ForeignKey('Provincies', models.DO_NOTHING, db_column='idprovincia')

    class Meta:
        managed = False
        db_table = 'comunitatsautonomesprovincies'


class Demarcacionsterritorials(models.Model):
    iddemarcacioterritorial = models.ForeignKey('Objectessipan', models.DO_NOTHING, db_column='iddemarcacioterritorial', primary_key=True)
    nomdemarcacioterritorial = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'demarcacionsterritorials'


class Municipis(models.Model):
    idmunicipi = models.ForeignKey('Objectessipan', models.DO_NOTHING, db_column='idmunicipi', primary_key=True)
    codiine = models.CharField(unique=True, max_length=6, blank=True, null=True)
    datamunicipi = models.DateField(blank=True, null=True)
    nommunicipi = models.CharField(max_length=255, blank=True, null=True)
    areaoficial = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    areareal = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    perimetrereal = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    perimetreoficial = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    idcomarca = models.ForeignKey(Comarques, models.DO_NOTHING, db_column='idcomarca', blank=True, null=True)
    idprovincia = models.ForeignKey('Provincies', models.DO_NOTHING, db_column='idprovincia', blank=True, null=True)
    nifcif = models.CharField(max_length=10, blank=True, null=True)
    idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipis'


class Pais(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'pais'


class Provincies(models.Model):
    idprovincia = models.ForeignKey('Objectessipan', models.DO_NOTHING, db_column='idprovincia', primary_key=True)
    codiprovincia = models.CharField(max_length=3, blank=True, null=True)
    nomprovincia = models.CharField(max_length=255)
    idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provincies'


class Tipusclassificaciosol(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipusclassificaciosol'

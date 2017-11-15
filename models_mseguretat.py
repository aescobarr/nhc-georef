# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Authority(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    authority = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authority'


class Bloquejosobjectessipan(models.Model):
    idbloqueigobjecte = models.CharField(max_length=100)
    idmodul = models.CharField(max_length=100)
    tipusobjecte = models.CharField(max_length=35)
    idobjectebloquejat = models.CharField(max_length=100)
    idusuari = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)
    timestamp_field = models.DateField(db_column='timestamp_', blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'bloquejosobjectessipan'


class Detallsusuari(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    idusuari = models.CharField(max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    cognom1 = models.CharField(max_length=100, blank=True, null=True)
    cognom2 = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detallsusuari'


class Filtrejson(models.Model):
    idfiltre = models.CharField(max_length=100)
    json = models.TextField(blank=True, null=True)
    modul = models.CharField(max_length=100, blank=True, null=True)
    nomfiltre = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filtrejson'


class Filtres(models.Model):
    idfiltre = models.CharField(max_length=100)
    idusuari = models.CharField(max_length=100)
    ip = models.CharField(max_length=15, blank=True, null=True)
    idmodul = models.CharField(max_length=100)
    tipusobjecte = models.CharField(max_length=25)
    idobjectesipan = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'filtres'


class Logactivitatobjectessipan(models.Model):
    idlog = models.CharField(primary_key=True, max_length=200)
    idusuari = models.ForeignKey('Usuaris', models.DO_NOTHING, db_column='idusuari')
    ip = models.CharField(max_length=15, blank=True, null=True)
    idmodul = models.CharField(max_length=100)
    tipusobjecte = models.CharField(max_length=35)
    idobjectesipan = models.CharField(max_length=200, blank=True, null=True)
    operacio = models.CharField(max_length=10)
    timestamp_field = models.DateField(db_column='timestamp_')  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'logactivitatobjectessipan'


class Registreusuaris(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idusuari = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)
    horaentrada = models.DateField(blank=True, null=True)
    horasortida = models.DateField(blank=True, null=True)
    idmodul = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registreusuaris'


class Rols(models.Model):
    idrol = models.CharField(primary_key=True, max_length=100)
    rol = models.CharField(max_length=100)
    idmodul = models.CharField(max_length=100)
    descripcio = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rols'


class Rolsaplicaciousuari(models.Model):
    idfuncionalitat = models.CharField(primary_key=True, max_length=100)
    funcionalitat = models.CharField(max_length=100)
    idmodul = models.CharField(max_length=100)
    idusuari = models.ForeignKey('Usuaris', models.DO_NOTHING, db_column='idusuari')

    class Meta:
        managed = False
        db_table = 'rolsaplicaciousuari'


class Rolsdadesusuari(models.Model):
    idroldadesusuari = models.CharField(primary_key=True, max_length=100)
    idrol = models.ForeignKey(Rols, models.DO_NOTHING, db_column='idrol')
    valorrol = models.CharField(max_length=500)
    idusuari = models.ForeignKey('Usuaris', models.DO_NOTHING, db_column='idusuari')
    editar = models.CharField(max_length=1, blank=True, null=True)
    inserir = models.CharField(max_length=1, blank=True, null=True)
    esborrar = models.CharField(max_length=1, blank=True, null=True)
    veure = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rolsdadesusuari'


class Usuariauthority(models.Model):
    idusuari = models.CharField(max_length=100, blank=True, null=True)
    idauthority = models.ForeignKey(Authority, models.DO_NOTHING, db_column='idauthority', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuariauthority'


class Usuaripermisediciotoponimauth(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    idusuari = models.CharField(max_length=100, blank=True, null=True)
    idauthority = models.CharField(max_length=100, blank=True, null=True)
    idtoponim = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuaripermisediciotoponimauth'


class Usuaris(models.Model):
    idusuari = models.CharField(primary_key=True, max_length=100)
    nomusuari = models.CharField(max_length=100)
    idtecnic = models.CharField(max_length=100, blank=True, null=True)
    idpersona = models.CharField(max_length=100, blank=True, null=True)
    idorganitzacio = models.CharField(max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    primercognom = models.CharField(max_length=100, blank=True, null=True)
    pwdsecure = models.CharField(max_length=200, blank=True, null=True)
    alta = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuaris'

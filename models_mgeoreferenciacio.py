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
        unique_together = (('id', 'id'), ('idambitgeografic', 'idrecursgeoref'),)


class Autorrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idrecursgeoref = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecursgeoref')
    idpersona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='idpersona')

    class Meta:
        managed = False
        db_table = 'autorrecursgeoref'
        unique_together = (('id', 'id'), ('idpersona', 'idrecursgeoref'),)


class Capawms(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    baseurlservidor = models.CharField(max_length=400)
    name = models.CharField(max_length=400)
    label = models.CharField(max_length=400, blank=True, null=True)
    minx = models.FloatField(blank=True, null=True)
    maxx = models.FloatField(blank=True, null=True)
    miny = models.FloatField(blank=True, null=True)
    maxy = models.FloatField(blank=True, null=True)
    boundary = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capawms'


class Capesrecurs(models.Model):
    idcapa = models.ForeignKey(Capawms, models.DO_NOTHING, db_column='idcapa', blank=True, null=True)
    idrecurs = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecurs', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capesrecurs'


class Conversio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'conversio'
        unique_together = (('id', 'id'),)


class DadesMunicipipuntradi(models.Model):
    municipi = models.CharField(max_length=250, blank=True, null=True)
    comarca = models.CharField(max_length=250, blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    precisio = models.FloatField(blank=True, null=True)
    xutm31ed50 = models.FloatField(blank=True, null=True)
    yutm31hnub = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dades_municipipuntradi'


class Documentsrecursos(models.Model):
    iddocument = models.ForeignKey('Documents', models.DO_NOTHING, db_column='iddocument', blank=True, null=True)
    idrecurs = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecurs', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentsrecursos'


class Documentsversions(models.Model):
    iddocument = models.ForeignKey('Documents', models.DO_NOTHING, db_column='iddocument', blank=True, null=True)
    idversio = models.ForeignKey('Toponimversio', models.DO_NOTHING, db_column='idversio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentsversions'


class Paraulaclau(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    paraula = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'paraulaclau'


class Paraulaclaurecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idrecursgeoref = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecursgeoref')
    idparaula = models.ForeignKey(Paraulaclau, models.DO_NOTHING, db_column='idparaula')

    class Meta:
        managed = False
        db_table = 'paraulaclaurecursgeoref'


class PrefsVisibilitatCapes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idusuari = models.ForeignKey('Usuaris', models.DO_NOTHING, db_column='idusuari', blank=True, null=True)
    prefscapesjson = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prefs_visibilitat_capes'


class Qualificadorversio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    qualificador = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'qualificadorversio'


class Recursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=500)
    idtipusrecursgeoref = models.ForeignKey('Tipusrecursgeoref', models.DO_NOTHING, db_column='idtipusrecursgeoref', blank=True, null=True)
    comentarisnoambit = models.CharField(max_length=500, blank=True, null=True)
    campidtoponim = models.CharField(max_length=500, blank=True, null=True)
    idsistemareferenciaepsg = models.ForeignKey('Sistemareferencia', models.DO_NOTHING, db_column='idsistemareferenciaepsg', blank=True, null=True)
    versio = models.CharField(max_length=100, blank=True, null=True)
    fitxergraficbase = models.CharField(max_length=100, blank=True, null=True)
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
    idambit = models.ForeignKey('Toponimversio', models.DO_NOTHING, db_column='idambit', blank=True, null=True)
    acronim = models.CharField(max_length=100, blank=True, null=True)
    idsistemareferenciamm = models.ForeignKey('Sistemareferenciamm', models.DO_NOTHING, db_column='idsistemareferenciamm', blank=True, null=True)
    idtipusunitatscarto = models.ForeignKey('Tipusunitats', models.DO_NOTHING, db_column='idtipusunitatscarto', blank=True, null=True)
    idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)
    base_url_wms = models.CharField(max_length=255, blank=True, null=True)
    capes_wms_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recursgeoref'
        unique_together = (('id', 'id'),)


class Recursgeoreftoponim(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref')
    idtoponim = models.ForeignKey('Toponim', models.DO_NOTHING, db_column='idtoponim', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recursgeoreftoponim'
        unique_together = (('idtoponim', 'idrecursgeoref'),)


class Registresrafel(models.Model):
    max = models.TextField(blank=True, null=True)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250, blank=True, null=True)
    datacaptura = models.DateField(blank=True, null=True)
    coordenada_x = models.FloatField(blank=True, null=True)
    coordenada_y = models.FloatField(blank=True, null=True)
    coordenada_z = models.FloatField(blank=True, null=True)
    precisio_h = models.FloatField(blank=True, null=True)
    precisio_z = models.FloatField(blank=True, null=True)
    idsistemareferenciarecurs = models.CharField(max_length=100, blank=True, null=True)
    coordenada_x_origen = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_origen = models.CharField(max_length=50, blank=True, null=True)
    coordenada_z_origen = models.CharField(max_length=50, blank=True, null=True)
    precisio_h_origen = models.CharField(max_length=50, blank=True, null=True)
    precisio_z_origen = models.CharField(max_length=50, blank=True, null=True)
    idpersona = models.CharField(max_length=100, blank=True, null=True)
    observacions = models.TextField(blank=True, null=True)
    idlimitcartooriginal = models.CharField(max_length=100, blank=True, null=True)
    idrecursgeoref = models.CharField(max_length=100, blank=True, null=True)
    idtoponim = models.CharField(max_length=200, blank=True, null=True)
    numero_versio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registresrafel'


class Sistemareferenciarecurs(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref')
    idsistemareferenciamm = models.ForeignKey('Sistemareferenciamm', models.DO_NOTHING, db_column='idsistemareferenciamm', blank=True, null=True)
    sistemareferencia = models.CharField(max_length=1000, blank=True, null=True)
    conversio = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sistemareferenciarecurs'


class Tipusrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipusrecursgeoref'


class Tipustoponim(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipustoponim'


class Toponim(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250)
    aquatic = models.CharField(max_length=1, blank=True, null=True)
    idtipustoponim = models.ForeignKey(Tipustoponim, models.DO_NOTHING, db_column='idtipustoponim')
    idpais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='idpais', blank=True, null=True)
    idpare = models.ForeignKey('self', models.DO_NOTHING, db_column='idpare', blank=True, null=True)
    nom_fitxer_importacio = models.CharField(max_length=255, blank=True, null=True)
    linia_fitxer_importacio = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponim'


class Toponimsexclosos(models.Model):
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim')
    idtoponimexclos = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponimexclos')

    class Meta:
        managed = False
        db_table = 'toponimsexclosos'


class Toponimsversiorecurs(models.Model):
    idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref', blank=True, null=True)
    idtoponimversio = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponimsversiorecurs'


class Toponimversio(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250)
    datacaptura = models.DateField(blank=True, null=True)
    coordenada_x = models.FloatField(blank=True, null=True)
    coordenada_y = models.FloatField(blank=True, null=True)
    coordenada_z = models.FloatField(blank=True, null=True)
    precisio_h = models.FloatField(blank=True, null=True)
    precisio_z = models.FloatField(blank=True, null=True)
    idsistemareferenciarecurs = models.ForeignKey(Sistemareferenciarecurs, models.DO_NOTHING, db_column='idsistemareferenciarecurs', blank=True, null=True)
    coordenada_x_origen = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_origen = models.CharField(max_length=50, blank=True, null=True)
    coordenada_z_origen = models.CharField(max_length=50, blank=True, null=True)
    precisio_h_origen = models.CharField(max_length=50, blank=True, null=True)
    precisio_z_origen = models.CharField(max_length=50, blank=True, null=True)
    idpersona = models.CharField(max_length=100, blank=True, null=True)
    observacions = models.TextField(blank=True, null=True)
    idlimitcartooriginal = models.ForeignKey('Documents', models.DO_NOTHING, db_column='idlimitcartooriginal', blank=True, null=True)
    idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref', blank=True, null=True)
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim', blank=True, null=True)
    numero_versio = models.IntegerField(blank=True, null=True)
    idqualificador = models.ForeignKey(Qualificadorversio, models.DO_NOTHING, db_column='idqualificador', blank=True, null=True)
    coordenada_x_centroide = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_centroide = models.CharField(max_length=50, blank=True, null=True)
    idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponimversio'


class ToponimversioBackup(models.Model):
    id = models.CharField(max_length=200, blank=True, null=True)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250, blank=True, null=True)
    datacaptura = models.DateField(blank=True, null=True)
    coordenada_x = models.FloatField(blank=True, null=True)
    coordenada_y = models.FloatField(blank=True, null=True)
    coordenada_z = models.FloatField(blank=True, null=True)
    precisio_h = models.FloatField(blank=True, null=True)
    precisio_z = models.FloatField(blank=True, null=True)
    idsistemareferenciarecurs = models.CharField(max_length=100, blank=True, null=True)
    coordenada_x_origen = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_origen = models.CharField(max_length=50, blank=True, null=True)
    coordenada_z_origen = models.CharField(max_length=50, blank=True, null=True)
    precisio_h_origen = models.CharField(max_length=50, blank=True, null=True)
    precisio_z_origen = models.CharField(max_length=50, blank=True, null=True)
    idpersona = models.CharField(max_length=100, blank=True, null=True)
    observacions = models.TextField(blank=True, null=True)
    idlimitcartooriginal = models.CharField(max_length=100, blank=True, null=True)
    idrecursgeoref = models.CharField(max_length=100, blank=True, null=True)
    idtoponim = models.CharField(max_length=200, blank=True, null=True)
    numero_versio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponimversio_backup'


class Versions(models.Model):
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim', blank=True, null=True)
    idversio = models.ForeignKey(Toponimversio, models.DO_NOTHING, db_column='idversio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versions'

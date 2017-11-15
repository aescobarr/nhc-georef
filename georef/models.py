from django.db import models


# Create your models here.
'''
class Toponim(models.Model):
    codi = models.CharField(max_length=150)
    nom = models.CharField(max_length=250)
    aquatic = models.CharField(max_length=1)
    #text = models.CharField(max_length=150)
    #approved = models.BooleanField(default=False)
'''


class Tipustoponim(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = 'tipustoponim'

    def __str__(self):
        return '%s' % (self.nom)


class Pais(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=200)

    class Meta:
        #managed = False
        db_table = 'pais'

    def __str__(self):
        return '%s' % (self.nom)


class Qualificadorversio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    qualificador = models.CharField(max_length=500)

    class Meta:
        #managed = False
        db_table = 'qualificadorversio'


class Sistemareferenciarecurs(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    #idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref')
    #idsistemareferenciamm = models.ForeignKey('Sistemareferenciamm', models.DO_NOTHING, db_column='idsistemareferenciamm', blank=True, null=True)
    sistemareferencia = models.CharField(max_length=1000, blank=True, null=True)
    conversio = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sistemareferenciarecurs'


class Toponim(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250)
    aquatic = models.CharField(max_length=1, blank=True, null=True)
    idtipustoponim = models.ForeignKey(Tipustoponim, models.DO_NOTHING, db_column='idtipustoponim')
    idpais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='idpais', blank=True, null=True)
    idpare = models.ForeignKey('self', models.DO_NOTHING, db_column='idpare', blank=True, null=True)
    nom_fitxer_importacio = models.CharField(max_length=255, blank=True, null=True)
    linia_fitxer_importacio = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'toponim'

    @property
    def aquatic_str(self):
        return "Sí" if self.aquatic == "S" else "No"

    @property
    def nom_str(self):
        return '%s - %s (%s) (%s)' % (self.nom, self.idpais, self.idtipustoponim, self.aquatic)

    def __str__(self):
        return '%s - %s (%s) (%s)' % (self.nom, self.idpais, self.idtipustoponim, self.aquatic)


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
    #idlimitcartooriginal = models.ForeignKey('Documents', models.DO_NOTHING, db_column='idlimitcartooriginal', blank=True, null=True)
    #idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref', blank=True, null=True)
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim', blank=True, null=True)
    numero_versio = models.IntegerField(blank=True, null=True)
    idqualificador = models.ForeignKey(Qualificadorversio, models.DO_NOTHING, db_column='idqualificador', blank=True, null=True)
    coordenada_x_centroide = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_centroide = models.CharField(max_length=50, blank=True, null=True)
    #idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        #db_table = 'toponimversio'



class Versions(models.Model):
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim', blank=True, null=True)
    idversio = models.ForeignKey(Toponimversio, models.DO_NOTHING, db_column='idversio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versions'
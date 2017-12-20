from django.db.models import Q
from django.contrib.gis.db import models
import uuid
import operator
from django.contrib.gis.geos import GEOSGeometry
import json
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.


def append_chain_query(accum_query, current_clause, condicio):
    join_op = None
    if accum_query is None:
        accum_query = current_clause
    else:
        if condicio['operador'] == 'and':
            join_op = operator.and_
        elif condicio['operador'] == 'or':
            join_op = operator.or_
        else:
            pass
        accum_query = join_op(accum_query,current_clause)
    return accum_query


def pkgen():
    return str(uuid.uuid4())


class Tipustoponim(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipustoponim'

    def __str__(self):
        return '%s' % (self.nom)


class Pais(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'pais'

    def __str__(self):
        return '%s' % (self.nom)


class Qualificadorversio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    qualificador = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'qualificadorversio'


class Sistemareferenciarecurs(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    #idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref')
    #idsistemareferenciamm = models.ForeignKey('Sistemareferenciamm', models.DO_NOTHING, db_column='idsistemareferenciamm', blank=True, null=True)
    sistemareferencia = models.CharField(max_length=1000, blank=True, null=True)
    conversio = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sistemareferenciarecurs'


def append_string_to_toponim(toponim, current_elements):
    if toponim.idpare:
        current_elements.append(toponim.idpare.id + '$' + toponim.idpare.nom)
        append_string_to_toponim(toponim.idpare, current_elements)
    else:
        pass


def compute_denormalized_toponim_tree_val(toponim):
        stack = []
        append_string_to_toponim(toponim, stack)
        denormalized_val = '#'.join(list(reversed(stack)))
        return denormalized_val


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
    denormalized_toponimtree = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponim'

    @property
    def aquatic_str(self):
        return "Sí" if self.aquatic == "S" else "No"

    @property
    def nom_str(self):
        return '%s - %s (%s) (%s)' % (self.nom, '' if self.idpais is None else self.idpais, self.idtipustoponim, 'Aquàtic' if self.aquatic=='S' else 'Terrestre')

    def get_denormalized_toponimtree(self):
        stack = []
        stack = self.denormalized_toponimtree.split('#')
        return stack

    def get_denormalized_toponimtree_clean(self):
        stack = self.get_denormalized_toponimtree()
        stack_clean = []
        for elem in stack:
            stack_clean.append(elem.split('$')[0])
        return stack_clean

    def crea_query_de_filtre(json_filtre):
        accum_query = None
        for condicio in json_filtre:
            if condicio['condicio'] == 'nom':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(nom__icontains=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(nom__icontains=condicio['valor']), condicio)
            elif condicio['condicio'] == 'tipus':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(idtipustoponim__id=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(idtipustoponim__id=condicio['valor']), condicio)
            elif condicio['condicio'] == 'pais':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(idpais__id=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(idpais__id=condicio['valor']), condicio)
            elif condicio['condicio'] == 'aquatic':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(aquatic=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(aquatic=condicio['valor']), condicio)
            elif condicio['condicio'] == 'geografic':
                # Es passa al constructor unicament el geometry del json
                # geo = GEOSGeometry('{"type":"Polygon","coordinates":[[[-5.800781,32.546813],[12.480469,41.508577],[-6.855469,48.224673],[-5.800781,32.546813]]]}')
                if condicio['valor'] != '':
                    geometria = GEOSGeometry(condicio['valor'])
                    # geometria = GEOSGeometry(json.dumps(condicio['valor']['features'][0]['geometry']))
                    if condicio['not'] == 'S':
                        accum_query = append_chain_query(accum_query,~Q(versions__geometries__geometria__within=geometria),condicio)
                    else:
                        accum_query = append_chain_query(accum_query,Q(versions__geometries__geometria__within=geometria), condicio)
        return accum_query

    def __str__(self):
        return '%s - %s (%s) (%s)' % (self.nom, self.idpais, self.idtipustoponim, self.aquatic)


class Tipusunitats(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    tipusunitat = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'tipusunitats'


class Tipusrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipusrecursgeoref'


class Suport(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'suport'


class Sistemareferenciamm(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'sistemareferenciamm'


class Recursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=500)
    idtipusrecursgeoref = models.ForeignKey('Tipusrecursgeoref', models.DO_NOTHING, db_column='idtipusrecursgeoref', blank=True, null=True)
    comentarisnoambit = models.CharField(max_length=500, blank=True, null=True)
    campidtoponim = models.CharField(max_length=500, blank=True, null=True)
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
    #idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)
    base_url_wms = models.CharField(max_length=255, blank=True, null=True)
    capes_wms_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recursgeoref'
        #unique_together = (('id', 'id'),)


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
    idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref', blank=True, null=True)
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim', blank=True, null=True, related_name='versions')
    numero_versio = models.IntegerField(blank=True, null=True)
    idqualificador = models.ForeignKey(Qualificadorversio, models.DO_NOTHING, db_column='idqualificador', blank=True, null=True)
    coordenada_x_centroide = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_centroide = models.CharField(max_length=50, blank=True, null=True)
    #idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponimversio'


'''
class Versions(models.Model):
    idtoponim = models.ForeignKey(Toponim, models.DO_NOTHING, db_column='idtoponim', blank=True, null=True)
    idversio = models.ForeignKey(Toponimversio, models.DO_NOTHING, db_column='idversio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versions'
'''

class Filtrejson(models.Model):
    idfiltre = models.CharField(primary_key=True, max_length=100, default=pkgen)
    json = models.TextField()
    modul = models.CharField(max_length=100)
    nomfiltre = models.CharField(max_length=200)

    @property
    def description(self):
        retval = 'Filtre buit!'
        if self.json and self.json != '':
            json_val = json.loads(self.json)
            filtre = json_val['filtre']
            filtre_text = []
            if len(filtre) > 0 :
                retVal = ''
                for elem in filtre:
                    op = elem['operador']
                    filtre_text.append(op)
                    negate = '' if elem['not'] == 'N' else 'NOT'
                    filtre_text.append(negate)
                    cond = elem['condicio']
                    filtre_text.append(cond)
                    filtre_text.append('=')
                    if cond.lower() == 'geografic' or cond.lower() == 'geografic_geo':
                        filtre_text.append('Poligon')
                    else:
                        filtre_text.append(elem['valor'])
            retval = ' '.join(filtre_text)
        return retval

    class Meta:
        managed = False
        db_table = 'filtrejson'


@receiver(pre_save, sender=Toponim)
def my_callback(sender, instance, *args, **kwargs):
    recalc_denormalized_toponim_tree = compute_denormalized_toponim_tree_val(instance)
    instance.denormalized_toponimtree = recalc_denormalized_toponim_tree

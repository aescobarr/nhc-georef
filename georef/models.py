from django.db.models import Q
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import uuid
import operator
from django.contrib.gis.geos import GEOSGeometry, Point
import json
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from georef.tasks import compute_denormalized_toponim_tree_val, format_denormalized_toponimtree, pkgen
from georef_addenda.models import Autor
from georef.geom_utils import *
import datetime
import itertools

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


class Tipustoponim(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    nom = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipustoponim'

    def __str__(self):
        return '%s' % (self.nom)


class Pais(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    nom = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'pais'

    def __str__(self):
        return '%s' % (self.nom)


class Qualificadorversio(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    qualificador = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'qualificadorversio'

    def __str__(self):
        return '%s' % (self.qualificador)


class Sistemareferenciarecurs(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    #idrecursgeoref = models.ForeignKey(Recursgeoref, models.DO_NOTHING, db_column='idrecursgeoref')
    #idsistemareferenciamm = models.ForeignKey('Sistemareferenciamm', models.DO_NOTHING, db_column='idsistemareferenciamm', blank=True, null=True)
    sistemareferencia = models.CharField(max_length=1000, blank=True, null=True)
    conversio = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sistemareferenciarecurs'


class Toponim(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=pkgen)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250)
    aquatic = models.CharField(max_length=1, blank=True, null=True, default='N')
    idtipustoponim = models.ForeignKey(Tipustoponim, models.DO_NOTHING, db_column='idtipustoponim')
    idpais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='idpais', blank=True, null=True)
    idpare = models.ForeignKey('self', models.DO_NOTHING, db_column='idpare', blank=True, null=True)
    nom_fitxer_importacio = models.CharField(max_length=255, blank=True, null=True)
    linia_fitxer_importacio = models.TextField(blank=True, null=True)
    denormalized_toponimtree = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponim'

    def get_darrera_versio(self):
        max = -1
        tv = None
        for versio in self.versions.all():
            if max == -1:
                max = versio.numero_versio
                tv = versio
            else:
                if max >= versio.numero_versio:
                    max = versio.numero_versio
                    tv = versio
        return tv

    @property
    def aquatic_str(self):
        return "Sí" if self.aquatic == "S" else "No"

    @property
    def aquatic_bool(self):
        return True if self.aquatic == "S" else False

    @property
    def nom_str(self):
        return '%s - %s (%s) (%s)' % (self.nom, '' if self.idpais is None else self.idpais, self.idtipustoponim, 'Aquàtic' if self.aquatic=='S' else 'Terrestre')

    def get_denormalized_toponimtree(self):
        #stack = []
        #stack = self.denormalized_toponimtree.split('#')
        #return stack
        return format_denormalized_toponimtree(self.denormalized_toponimtree)

    def can_i_edit(self, toponim_permission):
        '''
        Returns true if a given user has permission to edit this toponim based on his upper limit toponim edit permission
        :param toponim_permission: Id of the highest toponim the user is allowed to edit
        :return: True, if either this is the highest toponim the user is allowed to edit or this toponim is below. False
        otherwise
        '''
        #Wildcard permission
        if toponim_permission == '1':
            return True
        if toponim_permission == self.id or toponim_permission in self.denormalized_toponimtree:
            return True
        return False


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
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    tipusunitat = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'tipusunitats'

    def __str__(self):
        return '%s' % (self.tipusunitat)


class Tipusrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.nom)

    class Meta:
        managed = False
        db_table = 'tipusrecursgeoref'


class Suport(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.nom)

    class Meta:
        managed = False
        db_table = 'suport'


class Sistemareferenciamm(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'sistemareferenciamm'

    def __str__(self):
        return '%s' % (self.nom)


class PrefsVisibilitatCapes(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    #idusuari = models.ForeignKey('Usuaris', models.CASCADE, db_column='idusuari')
    iduser = models.ForeignKey(User, models.CASCADE, db_column='iduser', related_name='prefswms', unique=True)
    prefscapesjson = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prefs_visibilitat_capes'


class Toponimversio(models.Model):
    id = models.CharField(primary_key=True, max_length=200,default=uuid.uuid4)
    codi = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=250)
    datacaptura = models.DateField(blank=True, null=True, default=datetime.date.today)
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
    #idpersona is a legacy field - NEVER EVER EVER USE IT
    idpersona = models.CharField(max_length=100, blank=True, null=True)
    iduser = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, db_column='iduser')
    observacions = models.TextField(blank=True, null=True)
    #idlimitcartooriginal = models.ForeignKey('Documents', models.DO_NOTHING, db_column='idlimitcartooriginal', blank=True, null=True)
    idrecursgeoref = models.ForeignKey('Recursgeoref', models.DO_NOTHING, db_column='idrecursgeoref', blank=True, null=True)
    idtoponim = models.ForeignKey(Toponim, models.CASCADE, db_column='idtoponim', blank=True, null=True, related_name='versions')
    numero_versio = models.IntegerField(blank=True, null=True)
    idqualificador = models.ForeignKey(Qualificadorversio, models.DO_NOTHING, db_column='idqualificador', blank=True, null=True)
    coordenada_x_centroide = models.CharField(max_length=50, blank=True, null=True)
    coordenada_y_centroide = models.CharField(max_length=50, blank=True, null=True)
    last_version = models.BooleanField(default=False)
    #idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toponimversio'

    def union_geometry(self):
        geometries = self.geometries.all()
        unio_geometries = None
        for geometria in geometries:
            if geometria.geometria.valid:
                this_geometria = geometria.geometria
                if unio_geometries is None:
                    unio_geometries = this_geometria
                else:
                    unio_geometries = unio_geometries.union(this_geometria)
        return unio_geometries

    @property
    def centroide_x(self):
        centroide = self.union_geometry()
        if centroide:
            return centroide.centroid.x
        return None

    @property
    def centroide_y(self):
        centroide = self.union_geometry()
        if centroide:
            return centroide.centroid.y
        return None

    @property
    def get_coordenada_y_centroide(self):
        if self.coordenada_y_centroide is None or self.coordenada_y_centroide == '':
            return self.centroide_y
        else:
            return self.coordenada_y_centroide

    @property
    def get_coordenada_x_centroide(self):
        if self.coordenada_x_centroide is None or self.coordenada_x_centroide == '':
            return self.centroide_x
        else:
            return self.coordenada_x_centroide

    @property
    def get_incertesa_centroide(self):
        union = self.union_geometry()
        if union is None:
            return self.precisio_h
        else:
            if union is not None:
                centroid = union.centroid
                if centroid is not None:
                    dist_max = 0
                    vertexes = extract_coords(union.coords)
                    for vertex in vertexes:
                        dist = vertex.distance(centroid)
                        if dist > dist_max:
                            dist_max = dist
                    return dist_max
            return 0


class Paraulaclau(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4)
    paraula = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'paraulaclau'


class ParaulaclauRecurs(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4)
    idparaula = models.ForeignKey(Paraulaclau, on_delete=models.CASCADE, db_column='idparaula')
    idrecursgeoref = models.ForeignKey('Recursgeoref', on_delete=models.CASCADE, db_column='idrecursgeoref')

    class Meta:
        managed = False
        db_table = 'paraulaclaurecursgeoref'


class Autorrecursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4)
    recurs = models.ForeignKey('Recursgeoref', models.CASCADE, db_column='idrecursgeoref')
    autor = models.ForeignKey(Autor, models.CASCADE, db_column='idpersona')

    class Meta:
        managed = False
        db_table = 'autorrecursgeoref'
        unique_together = (('autor', 'recurs'),)


class Capawms(models.Model):
    id = models.CharField(primary_key=True, max_length=200,default=uuid.uuid4)
    baseurlservidor = models.CharField(max_length=400)
    name = models.CharField(max_length=400)
    label = models.CharField(max_length=400, blank=True, null=True)
    minx = models.FloatField(blank=True, null=True)
    maxx = models.FloatField(blank=True, null=True)
    miny = models.FloatField(blank=True, null=True)
    maxy = models.FloatField(blank=True, null=True)
    boundary = models.GeometryField(blank=True, null=True)

    def crea_query_de_filtre(json_filtre):
        query = None
        for criteri in json_filtre:
            ids_capes = Capesrecurs.objects.filter(idrecurs=criteri['idrecurs']).values_list('idcapa', flat=True)
            query = Q(id__in=ids_capes)
        return query

    class Meta:
        managed = False
        db_table = 'capawms'


class Capesrecurs(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4)
    idcapa = models.ForeignKey(Capawms, models.CASCADE, db_column='idcapa', blank=True, null=True, related_name='recursos')
    idrecurs = models.ForeignKey('Recursgeoref', models.CASCADE, db_column='idrecurs', blank=True, null=True, related_name='capes')

    class Meta:
        managed = False
        db_table = 'capesrecurs'


class Recursgeoref(models.Model):
    id = models.CharField(primary_key=True, max_length=100,default=uuid.uuid4)
    nom = models.CharField(max_length=500)
    idtipusrecursgeoref = models.ForeignKey(Tipusrecursgeoref, models.DO_NOTHING, db_column='idtipusrecursgeoref', blank=True, null=True)
    comentarisnoambit = models.CharField(max_length=500, blank=True, null=True)
    campidtoponim = models.CharField(max_length=500, blank=True, null=True)
    versio = models.CharField(max_length=100, blank=True, null=True)
    fitxergraficbase = models.CharField(max_length=100, blank=True, null=True)
    idsuport = models.ForeignKey(Suport, models.DO_NOTHING, db_column='idsuport', blank=True, null=True)
    urlsuport = models.CharField(max_length=250, blank=True, null=True)
    ubicaciorecurs = models.CharField(max_length=200, blank=True, null=True)
    actualitzaciosuport = models.CharField(max_length=250, blank=True, null=True)
    mapa = models.CharField(max_length=100, blank=True, null=True)
    comentariinfo = models.TextField(blank=True, null=True)
    comentariconsulta = models.TextField(blank=True, null=True)
    comentariqualitat = models.TextField(blank=True, null=True)
    classificacio = models.CharField(max_length=300, blank=True, null=True)
    divisiopoliticoadministrativa = models.CharField(max_length=300, blank=True, null=True)
    idambit = models.ForeignKey(Toponimversio, models.DO_NOTHING, db_column='idambit', blank=True, null=True)
    acronim = models.CharField(max_length=100, blank=True, null=True)
    idsistemareferenciamm = models.ForeignKey(Sistemareferenciamm, models.DO_NOTHING, db_column='idsistemareferenciamm', blank=True, null=True)
    idtipusunitatscarto = models.ForeignKey(Tipusunitats, models.DO_NOTHING, db_column='idtipusunitatscarto', blank=True, null=True)
    #idgeometria = models.ForeignKey('Geometria', models.DO_NOTHING, db_column='idgeometria', blank=True, null=True)
    base_url_wms = models.CharField(max_length=255, blank=True, null=True)
    capes_wms_json = models.TextField(blank=True, null=True)
    paraulesclau = models.ManyToManyField(Paraulaclau,through=ParaulaclauRecurs)
    autors = models.ManyToManyField(Autor,through=Autorrecursgeoref)
    capes_wms_recurs = models.ManyToManyField(Capawms,through=Capesrecurs)

    class Meta:
        managed = False
        db_table = 'recursgeoref'

    def __str__(self):
        return '%s' % (self.nom)

    def paraulesclau_str(self):
        p_str = []
        for paraula in self.paraulesclau.all():
            p_str.append(paraula.paraula)
        return (',').join(p_str)

    def autors_str(self):
        a_str = []
        for autor in self.autors.all():
            a_str.append(autor.nom)
        return (',').join(a_str)

    def crea_query_de_filtre(json_filtre):
        accum_query = None
        for condicio in json_filtre:
            if condicio['condicio'] == 'nom':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(nom__icontains=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(nom__icontains=condicio['valor']), condicio)
            elif condicio['condicio'] == 'acronim':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(acronim__icontains=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(acronim__icontains=condicio['valor']), condicio)
            elif condicio['condicio'] == 'paraulaclau':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(paraulesclau__paraula__icontains=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(paraulesclau__paraula__icontains=condicio['valor']), condicio)
            elif condicio['condicio'] == 'tipus':
                if condicio['not'] == 'S':
                    accum_query = append_chain_query(accum_query, ~Q(idtipusrecursgeoref__id=condicio['valor']), condicio)
                else:
                    accum_query = append_chain_query(accum_query, Q(idtipusrecursgeoref__id=condicio['valor']), condicio)
            elif condicio['condicio'] == 'geografic_geo':
                # Es passa al constructor unicament el geometry del json
                # geo = GEOSGeometry('{"type":"Polygon","coordinates":[[[-5.800781,32.546813],[12.480469,41.508577],[-6.855469,48.224673],[-5.800781,32.546813]]]}')
                if condicio['valor'] != '':
                    geometria = GEOSGeometry(condicio['valor'])
                    # geometria = GEOSGeometry(json.dumps(condicio['valor']['features'][0]['geometry']))
                    if condicio['not'] == 'S':
                        accum_query = append_chain_query(accum_query,~Q(geometries__geometria__within=geometria),condicio)
                    else:
                        accum_query = append_chain_query(accum_query,Q(geometries__geometria__within=geometria), condicio)
        return accum_query



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

    def crea_query_de_filtre(json_filtre):
        query = None
        for criteri in json_filtre:
            query = Q(modul=criteri['modul'])
        return query

    class Meta:
        managed = False
        db_table = 'filtrejson'


@receiver(pre_save, sender=Toponim)
def my_callback(sender, instance, *args, **kwargs):
    recalc_denormalized_toponim_tree = compute_denormalized_toponim_tree_val(instance)
    instance.denormalized_toponimtree = recalc_denormalized_toponim_tree


@receiver(post_delete, sender=Toponimversio)
def reassign_last_version(sender, instance, *args, **kwargs):
    versions = Toponimversio.objects.filter(idtoponim=instance.idtoponim)
    max = -1
    darrer = None
    for versio in versions:
        if versio.numero_versio > max:
            max = versio.numero_versio
            darrer = versio
    if darrer is not None:
        darrer.last_version = True
        darrer.save()
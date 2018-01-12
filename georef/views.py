from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader
from django.shortcuts import render
from rest_framework import status,viewsets
from georef.serializers import ToponimSerializer, FiltrejsonSerializer, RecursgeorefSerializer, ToponimVersioSerializer
from georef.models import Toponim, Filtrejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from querystring_parser import parser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import operator
import functools
from georef.models import Tipustoponim, Pais, Qualificadorversio, Toponimversio
import json
from json import dumps
import magic
import zipfile
from djangoref.settings import *
import glob,os
import ntpath
import shapefile
import djangoref.settings as conf
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from georef.forms import ToponimsUpdateForm, ToponimversioForm
from django.forms import formset_factory
from django.db import IntegrityError, transaction
from georef.tasks import compute_denormalized_toponim_tree_val, format_denormalized_toponimtree


def get_order_clause(params_dict, translation_dict=None):
    order_clause = []
    try:
        order = params_dict['order']
        if len(order) > 0:
            for key in order:
                sort_dict = order[key]
                column_index_str = sort_dict['column']
                if translation_dict:
                    column_name = translation_dict[params_dict['columns'][int(column_index_str)]['data']]
                else:
                    column_name = params_dict['columns'][int(column_index_str)]['data']
                direction = sort_dict['dir']
                if direction != 'asc':
                    order_clause.append('-' + column_name)
                else:
                    order_clause.append(column_name)
    except KeyError:
        pass
    return order_clause


def get_filter_clause(params_dict, fields, translation_dict=None):
    filter_clause = []
    try:
        q = params_dict['search']['value']
        if q != '':
            for field in fields:
                if translation_dict:
                    translated_field_name = translation_dict[field]
                    filter_clause.append( Q(**{translated_field_name+'__icontains':q}) )
                else:
                    filter_clause.append(Q(**{field + '__icontains': q}))
    except KeyError:
        pass
    return filter_clause

def generic_datatable_list_endpoint(request,search_field_list,queryClass, classSerializer, field_translation_dict=None, order_translation_dict=None):
    draw = request.query_params.get('draw', -1)
    start = request.query_params.get('start', 0)
    #length = request.query_params.get('length', 25)
    length = 25

    get_dict = parser.parse(request.GET.urlencode())

    order_clause = get_order_clause(get_dict, order_translation_dict)

    filter_clause = get_filter_clause(get_dict, search_field_list, field_translation_dict)

    q = None
    try:
        string_json = get_dict['filtrejson']
        json_filter_data = json.loads(string_json)
        q = queryClass.crea_query_de_filtre(json_filter_data['filtre'])
    except KeyError:
        pass

    queryset = queryClass.objects.all()

    if q:
        queryset = queryset.filter(q)

    if len(filter_clause) == 0:
        queryset = queryset.order_by(*order_clause)
    else:
        queryset = queryset.order_by(*order_clause).filter(functools.reduce(operator.or_, filter_clause))

    paginator = Paginator(queryset, length)

    recordsTotal = queryset.count()
    recordsFiltered = recordsTotal
    page = int(start) / int(length) + 1

    serializer = classSerializer(paginator.page(page), many=True)
    return Response({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data': serializer.data})


def index(request):
    return render(request, 'georef/index.html')


class ToponimVersioViewSet(viewsets.ModelViewSet):
    queryset = Toponimversio.objects.all()
    serializer_class = ToponimVersioSerializer


class ToponimViewSet(viewsets.ModelViewSet):
    serializer_class = ToponimSerializer

    def get_queryset(self):
        queryset = Toponim.objects.all()
        term = self.request.query_params.get('term', None)
        if term is not None:
            queryset = queryset.filter(nom__icontains=term)
        return queryset


class FiltrejsonViewSet(viewsets.ModelViewSet):
    serializer_class = FiltrejsonSerializer

    def get_queryset(self):
        queryset = Filtrejson.objects.all()
        term = self.request.query_params.get('term', None)
        if term is not None:
            queryset = queryset.filter(nomfiltre__icontains=term)
        return queryset

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RecursGeoRefViewSet(viewsets.ModelViewSet):
    serializer_class = RecursgeorefSerializer

@api_view(['GET'])
def check_filtre(request):
    if request.method == 'GET':
        nomfiltre = request.query_params.get('nomfiltre', None)
        if nomfiltre is None:
            content = {'status': 'KO', 'detail':'mandatory param missing'}
            return Response(data=content,status=400)
        else:
            try:
                f = Filtrejson.objects.get(nomfiltre=nomfiltre)
                content = {'status': 'KO', 'detail': f.idfiltre}
                return Response(data=content, status=400)
            except Filtrejson.DoesNotExist:
                content = {'status': 'KO', 'detail': 'exists_not'}
                return Response(data=content, status=200)


@api_view(['GET'])
def toponims_datatable_list(request):
    if request.method == 'GET':
        search_field_list = ('nom_str', 'aquatic_str', 'idtipustoponim.nom')
        sort_translation_list = {'nom_str' : 'nom', 'aquatic_str' : 'aquatic', 'idtipustoponim.nom' : 'idtipustoponim__nom' }
        field_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom' : 'idtipustoponim__nom' }
        response = generic_datatable_list_endpoint(request, search_field_list, Toponim, ToponimSerializer,field_translation_list,sort_translation_list)
        return response


@api_view(['GET'])
def toponimfilters_datatable_list(request):
    if request.method == 'GET':
        search_field_list = ('nomfiltre',)
        response = generic_datatable_list_endpoint(request, search_field_list, Filtrejson, FiltrejsonSerializer)
        return response


@api_view(['GET'])
def process_shapefile(request):
    if request.method == 'GET':
        path = request.query_params.get('path', None)
        if path is None:
            content = {'success': False, 'detail': 'mandatory param missing'}
            return Response(data=content, status=400)
        else:
            filepath = path
            filename = ntpath.basename(os.path.splitext(filepath)[0])
            presumed_zipfile = magic.from_file(filepath)
            if not presumed_zipfile.lower().startswith('zip archive'):
                content = {'success': False, 'detail': 'Fitxer zip incorrecte'}
                return Response(data=content, status=400)
            else:
                #Extract file
                zip_ref = zipfile.ZipFile(filepath, 'r')
                zip_ref.extractall(BASE_DIR + "/uploads/" + filename)
                zip_ref.close()
                #Find and import shapefile
                os.chdir(BASE_DIR + "/uploads/" + filename)
                for file in glob.glob("*.shp"):
                    presumed_shapefile = magic.from_file(BASE_DIR + "/uploads/" + filename + "/" + file)
                    if presumed_shapefile.lower().startswith('esri shapefile'):
                        sf = shapefile.Reader(BASE_DIR + "/uploads/" + filename + "/" + file)
                        fields = sf.fields[1:]
                        field_names = [field[0] for field in fields]
                        buffer = []
                        for sr in sf.shapeRecords():
                            atr = dict(zip(field_names, sr.record))
                            geom = sr.shape.__geo_interface__
                            buffer.append(dict(type="Feature", geometry=geom, properties=atr))
                        geojson = dumps({"type": "FeatureCollection", "features": buffer})
                        content = {'success': True, 'detail': geojson}
                        return Response(data=content, status=200)
                    else:
                        content = {'success': False, 'detail': 'El fitxer shapefile té un format incorrecte'}
                        return Response(data=content, status=200)
                content = {'success': False, 'detail': 'No he trobat cap fitxer amb extensió *.shp dins del zip, no puc importar res.'}
                return Response(data=content, status=200)


@login_required
def toponimfilters(request):
    csrf_token = get_token(request)
    return render(request, 'georef/toponimfilters_list.html', context={'csrf_token': csrf_token})


@login_required
def toponims(request):
    csrf_token = get_token(request)
    wms_url = conf.GEOSERVER_WMS_URL
    llista_tipus = Tipustoponim.objects.order_by('nom')
    llista_paisos = Pais.objects.order_by('nom')
    return render(request, 'georef/toponims_list.html', context={ 'llista_tipus': llista_tipus, 'llista_paisos': llista_paisos, 'csrf_token': csrf_token, 'wms_url':wms_url })


@login_required
def toponimstree(request):
    return render(request, 'georef/toponimstree.html')


def get_node_from_toponim(toponim):
    if Toponim.objects.filter(idpare=toponim.id).exists():
        toponim_node = { 'text' : toponim.nom_str, 'id': toponim.id, 'children':True}
    else:
        toponim_node = {'text': toponim.nom_str, 'id': toponim.id}
    return toponim_node


@api_view(['GET'])
def toponimstreenode(request):
    if request.method == 'GET':
        toponims = None
        data = []
        node_id = request.query_params.get('id', None)
        if node_id == '#':
            elem = {'text': 'Tots els topònims', 'id': '1', 'parent': '#', 'children' : True }
            return Response(data=elem, status=200)
        elif node_id == '1':
            toponims = Toponim.objects.filter(idpare__isnull=True).order_by('nom')
        else:
            toponims = Toponim.objects.filter(idpare=node_id).order_by('nom')
        for toponim in toponims:
            elem = get_node_from_toponim(toponim)
            data.append(elem)
        return Response(data=data, status=200)


'''
@login_required
def toponims_update(request, id=None):
    if id:
        toponim = get_object_or_404(Toponim,pk=id)
    else:
        raise forms.ValidationError("No existeix aquest topònim")
    form = ToponimsUpdateForm(request.POST or None, instance=toponim)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('toponims'))
    return render(request, 'georef/toponim_update.html', {'form': form, 'id' : id, 'nodelist_full': toponim.get_denormalized_toponimtree(), 'nodelist': toponim.get_denormalized_toponimtree_clean()})
'''

@login_required
def toponims_create(request):
    if request.method == 'POST':
        form = ToponimsUpdateForm(request.POST or None)
        if form.is_valid():
            form.save()
            url = reverse('toponims_update_2', kwargs = {'idtoponim': form.instance.id, 'idversio':'-1'})
            return HttpResponseRedirect(url)
    else:
        form = ToponimsUpdateForm()
    return render(request, 'georef/toponim_create.html', {'form': form, 'wms_url': conf.GEOSERVER_WMS_URL})

@login_required
def toponims_update_2(request, idtoponim=None, idversio=None):
    versio = None
    id_darrera_versio = None
    toponim = get_object_or_404(Toponim, pk=idtoponim)
    nodelist_full = format_denormalized_toponimtree(compute_denormalized_toponim_tree_val(toponim))
    toponimsversio = Toponimversio.objects.filter(idtoponim=toponim).order_by('-numero_versio')
    if request.method == 'GET':
        if idversio == '-1':
            if (len(toponimsversio) > 0):
                versio = toponimsversio[0]
                id_darrera_versio = versio.id
        elif idversio == '-2': #Afegint nova versió
            id_darrera_versio = '-2'
        else:
            versio = get_object_or_404(Toponimversio, pk=idversio)
            id_darrera_versio = idversio
        toponim_form = ToponimsUpdateForm(request.GET or None, instance=toponim)
        if versio:
            toponimversio_form = ToponimversioForm(request.GET or None, instance=versio)
        else:
            toponimversio_form = ToponimversioForm(request.GET or None)
        context = {
            'form': toponim_form,
            'toponimversio_form': toponimversio_form,
            'idtoponim': idtoponim,
            'idversio': idversio,
            'nodelist_full': nodelist_full,
            'versions': toponimsversio,
            'id_darrera_versio': id_darrera_versio
        }
        return render(request, 'georef/toponim_update_2.html', context)
    elif request.method == 'POST':
        if 'save_toponim_from_toponimversio' in request.POST:
            form = ToponimsUpdateForm(request.POST or None, instance=toponim)
            if form.is_valid():
                form.save()
                url = reverse('toponims_update_2', kwargs={'idtoponim': form.instance.id, 'idversio': idversio})
                return HttpResponseRedirect(url)
            else:
                if idversio == '-1':
                    if (len(toponimsversio) > 0):
                        versio = toponimsversio[0]
                        id_darrera_versio = versio.id
                else:
                    versio = get_object_or_404(Toponimversio, pk=idversio)
                    id_darrera_versio = idversio
                if versio:
                    toponimversio_form = ToponimversioForm(request.GET or None, instance=versio)
                else:
                    toponimversio_form = ToponimversioForm(request.GET or None)
                context = {
                    'form': form,
                    'toponimversio_form': toponimversio_form,
                    'idtoponim': idtoponim,
                    'idversio': idversio,
                    'nodelist_full': nodelist_full,
                    'versions': toponimsversio,
                    'id_darrera_versio': id_darrera_versio
                }
                return render(request, 'georef/toponim_update_2.html', context)
        elif 'save_versio_from_toponimversio' in request.POST:
            if idversio == '-1':
                if (len(toponimsversio) > 0):
                    versio = toponimsversio[0]
                    id_darrera_versio = versio.id
                else:
                    id_darrera_versio = -1
            elif idversio == '-2':
                id_darrera_versio = -2
            else:
                versio = get_object_or_404(Toponimversio, pk=idversio)
                id_darrera_versio = idversio
            if versio:
                toponimversio_form = ToponimversioForm(request.POST or None, instance=versio)
            else:
                toponimversio_form = ToponimversioForm(request.POST or None)
            form = ToponimsUpdateForm(request.POST or None, instance=toponim)
            if toponimversio_form.is_valid():
                toponimversio = toponimversio_form.save(commit=False)
                idversio = toponimversio.id
                toponimversio.idtoponim = toponim
                toponimversio.save()
                url = reverse('toponims_update_2', kwargs={'idtoponim': form.instance.id, 'idversio': idversio})
                return HttpResponseRedirect(url)
            else:
                context = {
                    'form': form,
                    'toponimversio_form': toponimversio_form,
                    'idtoponim': idtoponim,
                    'idversio': idversio,
                    'nodelist_full': nodelist_full,
                    'versions': toponimsversio,
                    'id_darrera_versio': id_darrera_versio
                }
                return render(request, 'georef/toponim_update_2.html', context)

@login_required
def toponims_update(request, id=None):
    toponim = get_object_or_404(Toponim, pk=id)
    nodelist_full = format_denormalized_toponimtree(compute_denormalized_toponim_tree_val(toponim))
    desat_amb_exit = False
    ToponimversioFormSet = formset_factory(ToponimversioForm,extra=0)
    toponimsversio = Toponimversio.objects.filter(idtoponim=toponim).order_by('-numero_versio')
    toponimsversio_data = [
        {
            'numero_versio': versio.numero_versio,
            'idqualificador': versio.idqualificador,
            'idrecursgeoref': versio.idrecursgeoref,
            'nom': versio.nom,
            'datacaptura': versio.datacaptura,
            'coordenada_x_origen': versio.coordenada_x_origen,
            'coordenada_y_origen': versio.coordenada_y_origen,
            'coordenada_z_origen': versio.coordenada_z_origen,
            'precisio_z_origen': versio.precisio_z_origen
        } for versio in toponimsversio
    ]
    toponim_form = ToponimsUpdateForm(request.POST or None, instance=toponim)
    toponimversio_form = ToponimversioFormSet(request.POST or None, initial=toponimsversio_data)
    if request.method == 'POST':
        if toponim_form.is_valid() and toponimversio_form.is_valid():
            toponim_form.save()
            versions = []
            for form in toponimversio_form:
                #toponimversio = form.instance
                toponimversio = Toponimversio(
                    numero_versio=form.cleaned_data.get('numero_versio'),
                    idqualificador=form.cleaned_data.get('idqualificador'),
                    idrecursgeoref=form.cleaned_data.get('idrecursgeoref'),
                    nom=form.cleaned_data.get('nom'),
                    datacaptura=form.cleaned_data.get('datacaptura'),
                    coordenada_x_origen=form.cleaned_data.get('coordenada_x_origen'),
                    coordenada_y_origen=form.cleaned_data.get('coordenada_y_origen'),
                    coordenada_z_origen=form.cleaned_data.get('coordenada_z_origen'),
                    precisio_z_origen=form.cleaned_data.get('precisio_z_origen'),
                    idtoponim=toponim
                )
                versions.append(toponimversio)
                try:
                    with transaction.atomic():
                        Toponimversio.objects.filter(idtoponim=toponim).delete()
                        Toponimversio.objects.bulk_create(versions)
                        desat_amb_exit = True
                except IntegrityError as e:
                    print(e)
    context = {
        'form': toponim_form,
        'tv_form': toponimversio_form,
        'id': id,
        'nodelist_full': nodelist_full,
        'saved_success': desat_amb_exit,
        'wms_url': conf.GEOSERVER_WMS_URL
    }
    return render(request, 'georef/toponim_update.html',context)

import_uploader = AjaxFileUploader()
from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader
from django.shortcuts import render
from rest_framework import status,viewsets
from georef.serializers import ToponimSerializer, FiltrejsonSerializer
from georef.models import Toponim, Filtrejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from querystring_parser import parser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import operator
import functools
from georef.models import Tipustoponim, Pais
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
from georef.forms import ToponimsUpdateForm


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


import_uploader = AjaxFileUploader()
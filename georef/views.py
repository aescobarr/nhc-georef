from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader
from django.shortcuts import render
from rest_framework import status,viewsets
from georef.serializers import ToponimSerializer, FiltrejsonSerializer, RecursgeorefSerializer, ToponimVersioSerializer, UserSerializer, ProfileSerializer
from georef.models import Toponim, Filtrejson, Recursgeoref
from georef_addenda.models import Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from querystring_parser import parser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
import operator
import functools
from georef.models import Tipustoponim, Pais, Qualificadorversio, Toponimversio, Tipusrecursgeoref
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
from georef.forms import ToponimsUpdateForm, ToponimversioForm, ProfileForm, UserForm, ChangePasswordForm, NewUserForm
from django.forms import formset_factory
from django.db import IntegrityError, transaction
from georef.tasks import compute_denormalized_toponim_tree_val, format_denormalized_toponimtree, compute_denormalized_toponim_tree_val_to_root
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from georef_addenda.models import GeometriaToponimVersio

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.staticfiles.templatetags.staticfiles import static

from weasyprint import HTML, CSS
import csv
import xlwt


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

"""
Request is a rest_framework request
"""
def generic_datatable_list_endpoint(request,search_field_list,queryClass, classSerializer, field_translation_dict=None, order_translation_dict=None, paginate=True):

    '''
    request.query_params works only for rest_framework requests, but not for WSGI requests. request.GET[key] works for
    both types of requests
    '''

    '''    
    draw = request.query_params.get('draw', -1)
    start = request.query_params.get('start', 0)
    '''
    draw = -1
    start = 0
    try:
        draw = request.GET['draw']
    except:
        pass
    try:
        start = request.GET['start']
    except:
        pass

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

    if paginate:
        paginator = Paginator(queryset, length)

        recordsTotal = queryset.count()
        recordsFiltered = recordsTotal
        page = int(start) / int(length) + 1

        serializer = classSerializer(paginator.page(page), many=True, context={'request':request})
    else:
        serializer = classSerializer(queryset, many=True, context={'request':request})
        recordsTotal = queryset.count()
        recordsFiltered = recordsTotal

    return Response({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data': serializer.data})


def index(request):
    return render(request, 'georef/index.html')


class ToponimVersioViewSet(viewsets.ModelViewSet):
    queryset = Toponimversio.objects.all()
    serializer_class = ToponimVersioSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        modul = self.request.query_params.get('modul', None)
        if term is not None:
            queryset = queryset.filter(nomfiltre__icontains=term)
        if modul is not None:
            queryset = queryset.filter(modul=modul)
        return queryset

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RecursGeoRefViewSet(viewsets.ModelViewSet):
    serializer_class = RecursgeorefSerializer

@api_view(['GET'])
def check_filtre(request):
    if request.method == 'GET':
        nomfiltre = request.query_params.get('nomfiltre', None)
        modul = request.query_params.get('modul', None)
        if nomfiltre is None:
            content = {'status': 'KO', 'detail':'mandatory param missing'}
            return Response(data=content,status=400)
        if modul is None:
            content = {'status': 'KO', 'detail': 'mandatory param missing'}
            return Response(data=content, status=400)
        else:
            try:
                f = Filtrejson.objects.get(nomfiltre=nomfiltre, modul=modul)
                content = {'status': 'OK', 'detail': f.idfiltre}
                return Response(data=content, status=400)
            except Filtrejson.DoesNotExist:
                content = {'status': 'KO', 'detail': 'exists_not'}
                return Response(data=content, status=200)

@api_view(['GET'])
def users_datatable_list(request):
    if request.method == 'GET':
        search_field_list = ('user.username', 'user.first_name', 'user.last_name', 'user.email')
        sort_translation_list = {'user.username':'user__username', 'user.first_name':'user__first_name', 'user.last_name':'user__last_name', 'user.email':'user__email'}
        field_translation_list = {'user.username':'user__username', 'user.first_name':'user__first_name', 'user.last_name':'user__last_name', 'user.email':'user__email'}
        response = generic_datatable_list_endpoint(request, search_field_list, Profile, ProfileSerializer, field_translation_list, sort_translation_list)
        return response

@api_view(['GET'])
def recursos_datatable_list(request):
    if request.method == 'GET':
        search_field_list = ('nom',)
        sort_translation_list = {}
        field_translation_list = {}
        response = generic_datatable_list_endpoint(request, search_field_list, Recursgeoref, RecursgeorefSerializer,field_translation_list,sort_translation_list)
        return response

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
            content = {'success': False, 'detail': 'Ruta de fitxer incorrecta o fitxer no trobat!'}
            return Response(data=content, status=400)
        else:
            filepath = path
            filename = ntpath.basename(os.path.splitext(filepath)[0])
            presumed_zipfile = magic.from_file(filepath)
            if not presumed_zipfile.lower().startswith('zip archive'):
                content = {'success': False, 'detail': 'No sembla que el fitxer sigui un zip correcte'}
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


'''
@api_view(['GET'])
def get_centroid_from_shapefile(request):
    if request.method == 'GET':
        path = request.query_params.get('path', None)
        if path is None:
            content = {'success': False, 'detail': 'Ruta de fitxer incorrecta o fitxer no trobat!'}
            return Response(data=content, status=400)
        else:
            filepath = path
            filename = ntpath.basename(os.path.splitext(filepath)[0])
            presumed_zipfile = magic.from_file(filepath)
            if not presumed_zipfile.lower().startswith('zip archive'):
                content = {'success': False, 'detail': 'No sembla que el fitxer sigui un zip correcte'}
                return Response(data=content, status=400)
            else:
                # Extract file
                zip_ref = zipfile.ZipFile(filepath, 'r')
                zip_ref.extractall(BASE_DIR + "/uploads/" + filename)
                zip_ref.close()
                # Find and import shapefile
                os.chdir(BASE_DIR + "/uploads/" + filename)
                for file in glob.glob("*.shp"):
                    presumed_shapefile = magic.from_file(BASE_DIR + "/uploads/" + filename + "/" + file)
                    if presumed_shapefile.lower().startswith('esri shapefile'):
                        sf = shapefile.Reader(BASE_DIR + "/uploads/" + filename + "/" + file)
                        fields = sf.fields[1:]
                        field_names = [field[0] for field in fields]
                        buffer = []
                        for sr in sf.shapeRecords():
                            geom = sr.shape.__geo_interface__
                            geojson = dumps(geom)
                            geosgeom = GEOSGeometry(geojson)
                            buffer.append(geosgeom)
                        gc = GeometryCollection(buffer)
                        centroid_geojson = dumps(gc.centroid.geojson)
                        content = {'success': True, 'detail': centroid_geojson}
                        return Response(data=content, status=200)
                    else:
                        content = {'success': False, 'detail': 'El fitxer shapefile té un format incorrecte'}
                        return Response(data=content, status=200)
                content = {'success': False,
                           'detail': 'No he trobat cap fitxer amb extensió *.shp dins del zip, no puc importar res.'}
                return Response(data=content, status=200)
'''

@login_required
def toponimfilters(request):
    csrf_token = get_token(request)
    return render(request, 'georef/toponimfilters_list.html', context={'csrf_token': csrf_token})

@login_required
def users_list(request):
    if request.user.profile and request.user.profile.permission_administrative == False:
        return HttpResponse(reverse(index))
    else:
        return render(request, 'georef/user_list.html')

@login_required
def recursos(request):
    csrf_token = get_token(request)
    llista_tipus = Tipusrecursgeoref.objects.order_by('nom')
    wms_url = conf.GEOSERVER_WMS_URL
    return render(request, 'georef/recursos_list.html', context={'llista_tipus': llista_tipus, 'wms_url': wms_url, 'csrf_token': csrf_token})

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
        this_user = request.user
        id_toponim = request.user.profile.toponim_permission
        try:
            toponim = Toponim.objects.get(pk=id_toponim)
            node_ini = toponim.id
            nodelist_full = format_denormalized_toponimtree(compute_denormalized_toponim_tree_val(toponim))
        except Toponim.DoesNotExist:
            node_ini = '1'
            nodelist_full = ['1']
        form = ToponimsUpdateForm()
    return render(request, 'georef/toponim_create.html', {'form': form, 'wms_url': conf.GEOSERVER_WMS_URL, 'node_ini': node_ini, 'nodelist_full': nodelist_full})


def toponimversio_geometries_to_geojson(toponimversio):
    geometries = toponimversio.geometries.all()
    geos = []
    for geom in geometries:
        geos.append({'type': 'Feature', 'properties': {}, 'geometry': json.loads(geom.geometria.json) })
    features = {
        'type': 'FeatureCollection',
        'features': geos
    }
    return json.dumps(features)

@login_required
def toponims_update_2(request, idtoponim=None, idversio=None):
    versio = None
    geometries_json = None
    id_darrera_versio = None
    toponim = get_object_or_404(Toponim, pk=idtoponim)
    nodelist_full = format_denormalized_toponimtree(compute_denormalized_toponim_tree_val(toponim))
    toponimsversio = Toponimversio.objects.filter(idtoponim=toponim).order_by('-numero_versio')
    this_user = request.user
    node_ini = '1'
    if this_user.profile.permission_toponim_edition == False:
        return HttpResponse('No tens permís per editar topònims. Operació no permesa.')
    else:
        if toponim.can_i_edit(this_user.profile.toponim_permission):
            node_ini = this_user.profile.toponim_permission
        else:
            toponim_mes_alt = Toponim.objects.get(pk=this_user.profile.toponim_permission)
            message = ('No tens permís per editar aquest topònim. El topònim més alt a l\'arbre que pots editar és %s i aquest està jeràrquicament per sobre. Operació no permesa.') % (toponim_mes_alt.nom_str)
            return HttpResponse(message)
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
            geometries_json = toponimversio_geometries_to_geojson(versio)
        else:
            toponimversio_form = ToponimversioForm(request.GET or None)
        context = {
            'geometries_json': geometries_json,
            'form': toponim_form,
            'toponimversio_form': toponimversio_form,
            'idtoponim': idtoponim,
            'idversio': idversio,
            'nodelist_full': nodelist_full,
            'versions': toponimsversio,
            'id_darrera_versio': id_darrera_versio,
            'node_ini': node_ini
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
                    geometries_json = toponimversio_geometries_to_geojson(versio)
                else:
                    toponimversio_form = ToponimversioForm(request.GET or None)
                context = {
                    'geometries_json': geometries_json,
                    'form': form,
                    'toponimversio_form': toponimversio_form,
                    'idtoponim': idtoponim,
                    'idversio': idversio,
                    'nodelist_full': nodelist_full,
                    'versions': toponimsversio,
                    'id_darrera_versio': id_darrera_versio,
                    'node_ini': node_ini
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
                geometries_json = toponimversio_geometries_to_geojson(versio)
            else:
                toponimversio_form = ToponimversioForm(request.POST or None)
            form = ToponimsUpdateForm(request.POST or None, instance=toponim)
            if toponimversio_form.is_valid():
                toponimversio = toponimversio_form.save(commit=False)
                toponimversio.geometries.clear()
                idversio = toponimversio.id
                toponimversio.idtoponim = toponim
                toponimversio.iduser = this_user
                toponimversio.save()

                json_geometry_string = request.POST["geometria"]
                json_geometry = json.loads(json_geometry_string)
                for feature in json_geometry['features']:
                    feature_geometry = GEOSGeometry(json.dumps(feature['geometry']))
                    g = GeometriaToponimVersio(idversio=toponimversio, geometria=feature_geometry)
                    g.save()

                url = reverse('toponims_update_2', kwargs={'idtoponim': form.instance.id, 'idversio': idversio})
                return HttpResponseRedirect(url)
            else:
                context = {
                    'geometries_json': geometries_json,
                    'form': form,
                    'toponimversio_form': toponimversio_form,
                    'idtoponim': idtoponim,
                    'idversio': idversio,
                    'nodelist_full': nodelist_full,
                    'versions': toponimsversio,
                    'id_darrera_versio': id_darrera_versio,
                    'node_ini': node_ini
                }
                return render(request, 'georef/toponim_update_2.html', context)


@login_required
def recursos_list_csv(request):
    search_field_list = ('nom',)
    sort_translation_list = {}
    field_translation_list = {}
    data = generic_datatable_list_endpoint(request, search_field_list, Recursgeoref, RecursgeorefSerializer, field_translation_list, sort_translation_list, paginate=False)

    records = data.data['data']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['nom'])
    for record in records:
        writer.writerow([record['nom']])

    return response

@login_required
def recursos_list_xls(request):
    search_field_list = ('nom',)
    sort_translation_list = {}
    field_translation_list = {}
    data = generic_datatable_list_endpoint(request, search_field_list, Recursgeoref, RecursgeorefSerializer, field_translation_list, sort_translation_list, paginate=False)
    records = data.data['data']

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="recursos.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Recursos')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nom', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for record in records:
        row_num += 1
        ws.write(row_num, 0, record['nom'], font_style)

    wb.save(response)
    return response

@login_required
def toponims_list_xls(request):
    search_field_list = ('nom_str', 'aquatic_str', 'idtipustoponim.nom')
    sort_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom': 'idtipustoponim__nom'}
    field_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom': 'idtipustoponim__nom'}
    data = generic_datatable_list_endpoint(request, search_field_list, Toponim, ToponimSerializer,field_translation_list, sort_translation_list, paginate=False)
    records = data.data['data']

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="toponims.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Toponims')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nom', 'Aquàtic?', 'Tipus', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for record in records:
        row_num += 1
        ws.write(row_num, 0, record['nom_str'], font_style)
        ws.write(row_num, 1, record['aquatic'], font_style)
        ws.write(row_num, 2, record['idtipustoponim']['nom'], font_style)

    wb.save(response)
    return response


@login_required
def recursos_list_pdf(request):
    search_field_list = ('nom',)
    sort_translation_list = {}
    field_translation_list = {}
    data = generic_datatable_list_endpoint(request, search_field_list, Recursgeoref, RecursgeorefSerializer, field_translation_list, sort_translation_list, paginate=False)

    records = data.data['data']
    html_string = render_to_string('georef/reports/recursos_list_pdf.html',
                                   {'title': 'Llistat de Recursos de georeferenciació', 'records': records})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response


@login_required
def toponims_list_pdf(request):
    search_field_list = ('nom_str', 'aquatic_str', 'idtipustoponim.nom')
    sort_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom': 'idtipustoponim__nom'}
    field_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom': 'idtipustoponim__nom'}
    data = generic_datatable_list_endpoint(request, search_field_list, Toponim, ToponimSerializer, field_translation_list, sort_translation_list,paginate=False)

    records = data.data['data']
    html_string = render_to_string('georef/reports/toponims_list_pdf.html', {'title': 'Llistat de topònims', 'records': records})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response

@login_required
def toponims_detail_pdf(request, idtoponim=None):

    toponim = get_object_or_404(Toponim,pk=idtoponim)

    html_string = render_to_string('georef/reports/toponim_detail_pdf.html',{'toponim':toponim})
    georef_css = CSS('georef/static/georef/css/georef.css')
    #simple_grid = CSS('georef/static/georef/css/grid/simple-grid.css')
    #styles = [simple_grid, georef_css]
    styles = [georef_css]

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf', stylesheets=styles)


    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response


@login_required
def toponims_list_csv(request):
    search_field_list = ('nom_str', 'aquatic_str', 'idtipustoponim.nom')
    sort_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom': 'idtipustoponim__nom'}
    field_translation_list = {'nom_str': 'nom', 'aquatic_str': 'aquatic', 'idtipustoponim.nom': 'idtipustoponim__nom'}
    data = generic_datatable_list_endpoint(request, search_field_list, Toponim, ToponimSerializer, field_translation_list, sort_translation_list, paginate=False)

    records = data.data['data']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['nom_toponim','aquatic?','tipus_toponim'])
    for record in records:
        writer.writerow([record['nom_str'], record['aquatic'], record['idtipustoponim']['nom']])

    return response

@login_required
def my_profile(request):
    successfully_saved = False
    this_user = request.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=this_user)
        if user_form.is_valid():
            user_form.save()
            successfully_saved = True
        else:
            successfully_saved = False
    else:
        user_form = UserForm(instance=this_user)
    return render(request, 'georef/profile.html',{'user_form': user_form, 'successfully_saved': successfully_saved})


@user_passes_test(lambda u: u.is_superuser)
@login_required
@transaction.atomic
def user_profile(request, user_id=None):
    nodelist_full = []
    this_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=this_user)
        profile_form = ProfileForm(request.POST, instance=this_user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            url = reverse('users_list')
            return HttpResponseRedirect(url)
    else:
        user_form = UserForm(instance=this_user)
        profile_form = ProfileForm(instance=this_user.profile)

    if this_user and this_user.profile and this_user.profile.toponim_permission:
        if this_user.profile.toponim_permission == '1':
            nodelist_full = ['1']
        else:
            toponim = get_object_or_404(Toponim, pk=this_user.profile.toponim_permission)
            nodelist_full = format_denormalized_toponimtree(compute_denormalized_toponim_tree_val_to_root(toponim,[]))
    return render(request, 'georef/user_profile.html', {'user_id': this_user.id,'user_form': user_form, 'profile_form': profile_form, 'nodelist_full': nodelist_full})


@login_required
def change_my_password(request):
    this_user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password_1']
            this_user.set_password(password)
            this_user.save()
            url = reverse('index')
            return HttpResponseRedirect(url)
    else:
        form = ChangePasswordForm()
    return render(request, 'georef/change_password.html', {'form': form, 'edited_user': None})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def change_password(request,user_id=None):
    this_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password_1']
            this_user.set_password(password)
            this_user.save()
            url = reverse('users_list')
            return HttpResponseRedirect(url)
    else:
        form = ChangePasswordForm()
    return render(request, 'georef/change_password.html', {'form': form, 'edited_user': this_user})


@user_passes_test(lambda u: u.is_superuser)
@login_required
@transaction.atomic
def user_new(request):
    nodelist_full = []
    if request.method == 'POST':
        user_form = NewUserForm(request.POST or None)
        profile_form = ProfileForm(request.POST or None)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user.profile.toponim_permission = profile.toponim_permission
            user.profile.permission_toponim_edition = profile.permission_toponim_edition
            user.profile.permission_administrative = profile.permission_administrative
            user.profile.permission_filter_edition = profile.permission_filter_edition
            user.profile.permission_recurs_edition = profile.permission_recurs_edition
            user.profile.permission_tesaure_edition = profile.permission_tesaure_edition
            user.save()
            url = reverse('users_list')
            return HttpResponseRedirect(url)
    else:
        user_form = NewUserForm()
        profile_form = ProfileForm()
    return render(request, 'georef/user_new.html', {'user_form': user_form, 'profile_form': profile_form, 'nodelist_full': nodelist_full})


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
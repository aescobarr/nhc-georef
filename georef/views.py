from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from georef.forms import ToponimsForm
from rest_framework import status,viewsets
from georef.serializers import ToponimSerializer, FiltrejsonSerializer
from django.shortcuts import get_object_or_404
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
from django.contrib.gis.geos import GEOSGeometry
import json


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


def get_q_de_condicio(condicio):
    query = None
    if condicio['condicio'] == 'nom':
        if condicio['not']=='N':
            query = Q(nom__icontains=condicio['valor'])
        else:
            query = ~Q(nom__icontains=condicio['valor'])
    return query


def crea_query_de_filtre(json_filtre):
    accum_query = None
    for condicio in json_filtre:
        #print(condicio)
        if condicio['condicio'] == 'nom':
            if condicio['not'] == 'S':
                accum_query = append_chain_query(accum_query, ~Q(nom__icontains=condicio['valor']),condicio)
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
            # geometria = GEOSGeometry(condicio['valor'])
            geometria = GEOSGeometry(json.dumps(condicio['valor']['features'][0]['geometry']))
            if condicio['not'] == 'S':
                accum_query = append_chain_query(accum_query, ~Q(versions__geometries__geometria__within=geometria), condicio)
            else:
                accum_query = append_chain_query(accum_query, Q(versions__geometries__geometria__within=geometria), condicio)
    return accum_query


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


def generic_datatable_list_endpoint(request,search_field_list,queryClass, classSerializer, field_translation_dict=None, order_translation_dict=None):
    draw = request.query_params.get('draw', -1)
    start = request.query_params.get('start', 0)
    #length = request.query_params.get('length', 25)
    length = 25

    get_dict = parser.parse(request.GET.urlencode())

    order_clause = get_order_clause(get_dict, order_translation_dict)

    filter_clause = get_filter_clause(get_dict, search_field_list, field_translation_dict)

    string_json = get_dict['filtrejson']
    json_filter_data = json.loads(string_json)

    '''
    q = None
    for condicio in json_filter_data['filtre']:
        q = get_q_de_condicio(condicio)
        print(condicio)
    '''

    q = crea_query_de_filtre(json_filter_data['filtre'])

    queryset = queryClass.objects.all()

    if q:
        queryset = queryset.filter(q)

    if len(filter_clause) == 0:
        #queryset = queryClass.objects.order_by(*order_clause)
        queryset = queryset.order_by(*order_clause)
    else:
        #queryset = queryClass.objects.order_by(*order_clause).filter(functools.reduce(operator.or_, filter_clause))
        queryset = queryset.order_by(*order_clause).filter(functools.reduce(operator.or_, filter_clause))


    paginator = Paginator(queryset, length)

    recordsTotal = queryset.count()
    recordsFiltered = recordsTotal
    page = int(start) / int(length) + 1

    serializer = classSerializer(paginator.page(page), many=True)
    return Response({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data': serializer.data})

# Create your views here.
def index(request):
    return render(request, 'georef/index.html')
    # if this is a POST request we need to process the form data
    # if request.method == 'POST':
        # create a form instance and populate it with data from the request:
    # form = ToponimsForm(request.POST)
        # check whether it's valid:
    # if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
    # form.save()
    # return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    # else:
    # form = ToponimsForm()

    # return render(request, 'georef/index.html', {'form': form})
    #return render(request, 'georef/index.html', {'form': form})


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


@login_required
def toponims(request):
    llista_tipus = Tipustoponim.objects.order_by('nom')
    llista_paisos = Pais.objects.order_by('nom')
    return render(request, 'georef/toponims_list.html', context={ 'llista_tipus': llista_tipus, 'llista_paisos': llista_paisos })
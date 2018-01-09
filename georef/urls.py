from django.conf.urls import url, include
from rest_framework import routers
from georef import views

from . import views

router = routers.DefaultRouter()
router.register(r'toponims', views.ToponimViewSet, base_name='toponims')
router.register(r'filtres', views.FiltrejsonViewSet, base_name='filtres')
router.register(r'recursgeoref', views.RecursGeoRefViewSet, base_name='recursgeoref')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api_internal/',include(router.urls)),
    url(r'^datatabletoponims/list$', views.toponims_datatable_list, name='toponims_datatable_list'),
    url(r'^datatabletoponimfilters/list$', views.toponimfilters_datatable_list, name='toponimfilters_datatable_list'),
    url(r'^filtres/check$', views.check_filtre, name='check_filtre'),
    url(r'^toponims$', views.toponims, name='toponims'),
    url(r'^toponims/update/(?P<id>[0-9A-Za-z_\-]+)/$', views.toponims_update, name='toponims_update'),
    url(r'^toponims/update/(?P<idtoponim>[0-9A-Za-z_\-]+)/(?P<idversio>[0-9A-Za-z_\-]+)/$', views.toponims_update_2, name='toponims_update_2'),
    url(r'^toponimstree$', views.toponimstree, name='toponimstree'),
    #url(r'^toponimstree/(?P<node_id>[\w\-]+)/$', views.toponimstreenode, name='toponimstreenode'),
    url(r'^toponimstree/$', views.toponimstreenode, name='toponimstreenode'),
    url(r'^toponimfilters$', views.toponimfilters, name='toponimfilters'),
    url(r'ajax-upload$', views.import_uploader, name='ajax_upload'),
    url(r'ajax-process-shapefile$', views.process_shapefile, name='process_shapefile'),
]
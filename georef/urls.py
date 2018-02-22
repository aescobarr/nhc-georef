from django.conf.urls import url, include
from rest_framework import routers
from georef import views

from . import views

router = routers.DefaultRouter()
router.register(r'toponims', views.ToponimViewSet, base_name='toponims')
router.register(r'filtres', views.FiltrejsonViewSet, base_name='filtres')
router.register(r'recursgeoref', views.RecursGeoRefViewSet, base_name='recursgeoref')
router.register(r'versions', views.ToponimVersioViewSet, base_name='versions')
router.register(r'users', views.ProfileViewSet, base_name='users')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api_internal/',include(router.urls)),
    url(r'^datatabletoponims/list$', views.toponims_datatable_list, name='toponims_datatable_list'),
    url(r'^datatableusers/list$', views.users_datatable_list, name='users_datatable_list'),
    url(r'^datatabletoponimfilters/list$', views.toponimfilters_datatable_list, name='toponimfilters_datatable_list'),
    url(r'^filtres/check$', views.check_filtre, name='check_filtre'),
    url(r'^toponims$', views.toponims, name='toponims'),
    url(r'^toponims/update/(?P<id>[0-9A-Za-z_\-]+)/$', views.toponims_update, name='toponims_update'),
    url(r'^toponims/update/(?P<idtoponim>[0-9A-Za-z_\-]+)/(?P<idversio>[0-9A-Za-z_\-]+)/$', views.toponims_update_2, name='toponims_update_2'),
    url(r'^toponims/create/$', views.toponims_create, name='toponims_create'),
    url(r'^toponims/list/pdf/$', views.toponims_list_pdf, name='toponims_list_pdf'),
    url(r'^toponims/list/csv/$', views.toponims_list_csv, name='toponims_list_csv'),
    url(r'^toponims/list/xls/$', views.toponims_list_xls, name='toponims_list_xls'),
    url(r'^users/list/$', views.users_list, name='users_list'),
    url(r'^toponimstree$', views.toponimstree, name='toponimstree'),
    #url(r'^toponimstree/(?P<node_id>[\w\-]+)/$', views.toponimstreenode, name='toponimstreenode'),
    url(r'^toponimstree/$', views.toponimstreenode, name='toponimstreenode'),
    url(r'^toponimfilters$', views.toponimfilters, name='toponimfilters'),
    url(r'^user/profile/$', views.user_profile, name='user_profile'),
    url(r'ajax-upload$', views.import_uploader, name='ajax_upload'),
    url(r'ajax-process-shapefile$', views.process_shapefile, name='process_shapefile'),
]
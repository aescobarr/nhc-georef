from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from georef import views
from django.conf import settings

from . import views

router = routers.DefaultRouter()
router.register(r'toponims', views.ToponimViewSet, base_name='toponims')
router.register(r'toponimsearch', views.ToponimSearchViewSet, base_name='toponimsearch')
router.register(r'filtres', views.FiltrejsonViewSet, base_name='filtres')
router.register(r'recursgeoref', views.RecursGeoRefViewSet, base_name='recursgeoref')
router.register(r'versions', views.ToponimVersioViewSet, base_name='versions')
router.register(r'users', views.UsersViewSet, base_name='users')
router.register(r'paraulesclau', views.ParaulaClauViewSet, base_name='paraulesclau')
router.register(r'autors', views.AutorViewSet, base_name='autors')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api_internal/',include(router.urls)),
    url(r'^datatabletoponims/list$', views.toponims_datatable_list, name='toponims_datatable_list'),
    url(r'^datatablerecursos/list$', views.recursos_datatable_list, name='recursos_datatable_list'),
    url(r'^datatableusers/list$', views.users_datatable_list, name='users_datatable_list'),
    url(r'^datatabletoponimfilters/list$', views.filters_datatable_list, name='toponimfilters_datatable_list'),
    url(r'^datatablerecursfilters/list$', views.filters_datatable_list, name='recursfilters_datatable_list'),
    url(r'^datatablecapeswmslocals/list$', views.capeswmslocals_datatable_list, name='capeswmslocals_datatable_list'),
    url(r'^filtres/check$', views.check_filtre, name='check_filtre'),
    url(r'^wmsmetadata/$', views.wmsmetadata, name='wmsmetadata'),
    url(r'^wmslocal/create/$', views.wmslocal_create, name='wmslocal_create'),
    url(r'^wmslocal/delete/$', views.wmslocal_delete, name='wmslocal_delete_noparam'),
    url(r'^wmslocal/delete/(?P<id>[0-9A-Za-z_\-]+)/$', views.wmslocal_delete, name='wmslocal_delete'),
    url(r'^prefsvisualitzaciowms/$', views.prefsvisualitzaciowms, name='prefsvisualitzaciowms'),
    url(r'^prefsvisualitzaciowms/toggle/$', views.toggle_prefs_wms, name='toggle_prefs_wms'),
    url(r'^recursos$', views.recursos, name='recursos'),
    url(r'^recursos/create/$', views.recursos_create, name='recursos_create'),
    url(r'^recursos/update/(?P<id>[0-9A-Za-z_\-]+)/$', views.recursos_update, name='recursos_update'),
    url(r'^recursos/capeswms/$', views.recursos_capeswms, name='recursos_capeswms'),
    url(r'^toponims$', views.toponims, name='toponims'),
    url(r'^toponims/update/(?P<id>[0-9A-Za-z_\-]+)/$', views.toponims_update, name='toponims_update'),
    url(r'^toponims/update/(?P<idtoponim>[0-9A-Za-z_\-]+)/(?P<idversio>[0-9A-Za-z_\-]+)/$', views.toponims_update_2, name='toponims_update_2'),
    url(r'^toponims/create/$', views.toponims_create, name='toponims_create'),
    url(r'^toponims/search/$', views.toponims_search, name='toponims_search'),
    url(r'^toponims/list/pdf/$', views.toponims_list_pdf, name='toponims_list_pdf'),
    url(r'^toponims/detail/pdf/(?P<idtoponim>[0-9A-Za-z_\-]+)/$', views.toponims_detail_pdf, name='toponims_detail_pdf'),
    url(r'^toponims/list/csv/$', views.toponims_list_csv, name='toponims_list_csv'),
    url(r'^toponims/list/xls/$', views.toponims_list_xls, name='toponims_list_xls'),
    url(r'^toponims/import/$', views.toponims_import, name='toponims_import'),
    url(r'^recursos/list/xls/$', views.recursos_list_xls, name='recursos_list_xls'),
    url(r'^recursos/list/csv/$', views.recursos_list_csv, name='recursos_list_csv'),
    url(r'^recursos/list/pdf/$', views.recursos_list_pdf, name='recursos_list_pdf'),
    url(r'^users/list/$', views.users_list, name='users_list'),
    url(r'^toponimstree$', views.toponimstree, name='toponimstree'),
    url(r'^calculcentroides', views.calculcentroides, name='calculcentroides'),
    url(r'^computecentroid/(?P<file_name>[\w.]{0,256})$', views.compute_shapefile_centroid, name='compute_shapefile_centroid'),
    url(r'^computecentroid/$', views.compute_shapefile_centroid, name='compute_shapefile_centroid_noparams'),
    url(r'^importtoponims/(?P<file_name>[\w.]{0,256})$', views.import_toponims, name='import_toponims'),
    url(r'^importtoponims/$', views.import_toponims, name='import_toponims'),
    #url(r'^toponimstree/(?P<node_id>[\w\-]+)/$', views.toponimstreenode, name='toponimstreenode'),
    url(r'^toponimstree/$', views.toponimstreenode, name='toponimstreenode'),
    url(r'^toponimfilters$', views.toponimfilters, name='toponimfilters'),
    url(r'^recursfilters$', views.recursfilters, name='recursfilters'),
    url(r'^user/my_profile/$', views.my_profile, name='my_profile'),
    url(r'^user/profile/$', views.user_profile, name='user_profile'),
    url(r'^user/profile/(?P<user_id>[0-9A-Za-z_\-]+)/$', views.user_profile, name='user_profile'),
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^user/password/change_mine$', views.change_my_password, name='change_my_password'),
    url(r'^user/password/change$', views.change_password, name='change_password'),
    url(r'^user/password/change/(?P<user_id>[0-9A-Za-z_\-]+)/$', views.change_password, name='change_password'),
    url(r'ajax-upload$', views.import_uploader, name='ajax_upload'),
    url(r'ajax-process-shapefile$', views.process_shapefile, name='process_shapefile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
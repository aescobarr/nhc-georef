"""djangoref URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from georef import views
from django.contrib.auth.views import login,logout

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^', include('georef.urls')),
    #url(r'^georef/', include('georef.urls')),
    #url(r'^accounts/login/$', login, name='login'),
    #url(r'^logout/$', logout, {'next_page': '/accounts/login'}, name='logout'),
    url(r'^admin/', admin.site.urls),
]

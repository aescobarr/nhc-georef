# coding=utf-8
import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from georef.models import Toponimversio


for tv in Toponimversio.objects.all():
  print('Toponimversio id - ' + tv.id)
  for geometria in tv.geometries.all():
    print(geometria.geometria)
import os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from georef.models import Toponimversio

versions = Toponimversio.objects.all()

for versio in versions:
    if versio.last_version:
        if versio.iduser:
            org = versio.iduser.profile.organization
            versio.idtoponim.idorganization = org
            versio.idtoponim.save()
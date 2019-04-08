# coding=utf-8
import os, sys
from django.db import connection
from slugify import slugify


########################################################################################################################

# This script fills empty denormalized_toponim_tree fields in toponim table with the appropiate values

########################################################################################################################

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from georef.models import Toponim
from georef.tasks import compute_denormalized_toponim_tree_val


# toponims = Toponim.objects.all()
#
# for toponim in toponims:
#     if toponim.denormalized_toponimtree is None:
#         toponim.denormalized_toponimtree = compute_denormalized_toponim_tree_val(toponim)
#         toponim.save()

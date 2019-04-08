# coding=utf-8
import os, sys
from django.db import connection
from slugify import slugify


########################################################################################################################

# BEFORE RUNNING THIS SCRIPT, MAKE SURE THE FIELD TOPONIMVERSIO.IDUSER EXISTS!! IF NOT, CREATE IT!

########################################################################################################################

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.contrib.auth.models import User

user_correspondence = {}

with connection.cursor() as cursor:
    cursor.execute("""
        select du.idusuari, du.nom, du.cognom1, du.cognom2, du.email, u.nomusuari 
        from 
        public.detallsusuari du, public.usuaris u where u.idusuari = du.idusuari
    """)
    old_user_list = cursor.fetchall()

for old_user in old_user_list:
    u = User.objects.get(username = old_user[5],first_name=old_user[1],last_name=old_user[2],email=old_user[4])
    user_correspondence[old_user[0]]=u.id
    print(old_user)

print(user_correspondence)


for key in user_correspondence.keys():
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE prefs_visibilitat_capes set iduser=%s where idusuari=%s
        """, [ user_correspondence[key], key ])
#create new users and gather new ids. Produce table with new_id -> old_id
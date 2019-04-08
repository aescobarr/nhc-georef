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
    u = User(username = old_user[5],first_name=old_user[1],last_name=old_user[2],email=old_user[4])
    u.set_password('RzQ2C5uHjV9pkzLa')
    u.save()
    user_correspondence[old_user[0]]=u.id
    print(old_user)

print(user_correspondence)
#create new users and gather new ids. Produce table with new_id -> old_id

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT u.idusuari,ua.idauthority 
        from 
        public.usuaris u, public.usuariauthority ua where u.idusuari = ua.idusuari 
    """)
    old_permissions = cursor.fetchall()

print("Loaded old permissions")

'''
ROLE_ADMINISTRADOR_ADMINISTRACIO
ROLE_EDICIO
ROLE_EDICIO_FILTRES
ROLE_VISUALITZACIO
'''
print ("Updating profiles...")
for old_permission in old_permissions:
    id_old_user = old_permission[0]
    try:
        id_new_user = user_correspondence[id_old_user]
        u = User.objects.get(pk=id_new_user)
        if old_permission[1] == 'ROLE_ADMINISTRADOR_ADMINISTRACIO':
            u.profile.permission_administrative = True
        elif old_permission[1] == 'ROLE_EDICIO':
            u.profile.permission_toponim_edition = True
        elif old_permission[1] == 'ROLE_EDICIO_FILTRES':
            u.profile.permission_filter_edition = True
        #elif old_permission[1] ==  'ROLE_VISUALITZACIO':
        #    pass
        u.profile.save()
    except KeyError:
        print ( "Old user with id %s does not have a correspondent new user" % id_old_user )
print ("Profiles updated")


print ("Updating toponim edicio permissions...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT * from usuaripermisediciotoponimauth
    """)
    edicio_toponim_permissions = cursor.fetchall()

for old_edicio_toponim_permission in edicio_toponim_permissions:
    id_old_user = old_edicio_toponim_permission[1]
    id_new_user = user_correspondence[id_old_user]
    u = User.objects.get(pk=id_new_user)
    u.profile.toponim_permission = old_edicio_toponim_permission[3]
    u.profile.save()

print ("Toponim edicio permissions updated")


with connection.cursor() as cursor:
    cursor.execute("""
        SELECT * from sipan_msipan.personafisica where id in (select distinct idpersona from public.toponimversio)
    """)
    persones_fisiques = cursor.fetchall()


user_person_correspondence = {}

#try to find corresponding user
for persona in persones_fisiques:
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT * from auth_user where first_name=%s and last_name=%s
            """, [persona[2],persona[3]])
        pressumed_user = cursor.fetchall()
        if len(pressumed_user) == 0:
            print( persona[2] + " " + persona[3] + " person doesn't have a corresponding user, creating inactive user" )
            u = User(username=slugify(persona[2]),first_name=persona[2],last_name=persona[3],is_active=False)
            u.save()
            user_person_correspondence[persona[0]] = u.id
        elif len(pressumed_user) == 1:
            print( persona[2] + " " + persona[3] + " person exists as user, assigning")
            user = pressumed_user[0]
            user_person_correspondence[persona[0]] = user[0]


for key in user_person_correspondence.keys():
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE toponimversio set iduser=%s where idpersona=%s
        """, [ user_person_correspondence[key], key ])


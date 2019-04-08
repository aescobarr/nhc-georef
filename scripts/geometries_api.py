# coding=utf-8
import os, sys

########################################################################
# CREATES THE PRE_PROCESSED TOPONIMS TABLE TO BE CONSUMED BY THE API   #
########################################################################

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from georef.models import Toponimversio, Toponim
from django.db import connection
from georef.geom_utils import *

rows_insert = []
for toponim in Toponim.objects.all():
    id = toponim.id

    tv = toponim.get_darrera_versio()

    if tv is not None:
        geom = tv.union_geometry()
        if geom is not None:
            print(geom.wkt)
            rows_insert.append([id, geom.wkt])



cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS geometries_api cascade")

cursor.execute("""
    create table geometries_api(
        id character varying(200) NOT NULL PRIMARY KEY,
        geometria geometry(Geometry,4326) NOT NULL
    )
""")

for row in rows_insert:
    cursor.execute("""
        INSERT INTO geometries_api 
        (id, geometria) 
        values 
        (%s, ST_GeomFromText(%s,4326) )
    """, (row[0],row[1],) )


cursor.execute("""
    CREATE INDEX geometries_api_idx
    ON public.geometries_api
    USING gist
    (geometria)
        """)
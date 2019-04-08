import os, sys
from django.db import connection
from slugify import slugify

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoref.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

def insert_geometry(coord_x,coord_y,idversio):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            insert into georef_addenda_geometriatoponimversio(geometria,idversio)
            values
            ( ST_GEOMFromText('POINT(%s %s)',4326), %s )
            """, (float(coord_x), float(coord_y), idversio))
        print("Inserted geometry for " + idversio)

def geometria_is_empty(idgeometria):
    with connection.cursor() as cursor:
        cursor.execute("""
            select idpolipunt,idpolilinia,idpolipoligon from geometria where idgeometria = %s
        """,(idgeometria,))
        results = cursor.fetchone()
        if results is None or len(results) == 0:
            return True
        else:
            polipunts = False
            polilinies = False
            polipoligons = False
            idpolipunt = results[0]
            idpolilinia = results[1]
            idpolipoligon = results[2]
            #check polipunt
            with connection.cursor() as cursor:
                cursor.execute("""
                    select * from puntspolipunts where idpolipunt = %s
                    """, (idpolipunt,))
                results = cursor.fetchone()
                if results is not None and len(results) > 0:
                    polipunts = True
            # check polilinia
            with connection.cursor() as cursor:
                cursor.execute("""
                    select *
                    from 
                    liniespolilinies lpl,
                    linies l
                    where
                    lpl.idlinia = l.idlinia and
                    lpl.idpolilinia = %s
                """, (idpolilinia,))
                results = cursor.fetchone()
                if results is not None and len(results) > 0:
                    polilinies = True
            #check polipoligon
            with connection.cursor() as cursor:
                cursor.execute("""
                    select *
                    from
                    poligonspolipoligons
                    ppl,
                    poligons
                    p
                    where
                    ppl.idpoligon = p.idpoligon
                    and 
                    ppl.idpolipoligon = %s
                    """, (idpolipoligon,))
                results = cursor.fetchone()
                if results is not None and len(results) > 0:
                    polipoligons = True
            if polipunts or polilinies or polipoligons:
                return False
        return True




application = get_wsgi_application()


with connection.cursor() as cursor:
    cursor.execute("""
        select * from toponimversio where idgeometria is not null and 
        coordenada_x_centroide is not null and 
        coordenada_y_centroide is not null and 
        precisio_h is not null
    """)
    version_candidates = cursor.fetchall()

for row in version_candidates:
    idgeometria = row[24]
    if geometria_is_empty(idgeometria):
        print( idgeometria + " is empty")
        insert_geometry( row[22], row[23], row[0] )
from django.db import models
from django.contrib.gis.db import models
from georef.models import Toponimversio

# Create your models here.
class GeometriaToponimVersio(models.Model):
    idversio = models.ForeignKey(Toponimversio, on_delete=models.CASCADE, db_column='idversio', blank=True, null=True, related_name='geometries')
    geometria = models.GeometryField(srid=4326)

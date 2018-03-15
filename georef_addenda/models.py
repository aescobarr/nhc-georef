from django.db import models
from django.contrib.gis.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
#from georef.models import Toponim, Recursgeoref, Toponimversio, pkgen
from georef.tasks import pkgen


# Create your models here.
class GeometriaToponimVersio(models.Model):
    idversio = models.ForeignKey('georef.Toponimversio', on_delete=models.CASCADE, db_column='idversio', blank=True, null=True, related_name='geometries')
    geometria = models.GeometryField(srid=4326)


class GeometriaRecurs(models.Model):
    idrecurs = models.ForeignKey('georef.Recursgeoref', on_delete=models.CASCADE, db_column='idrecurs', blank=True, null=True, related_name='geometries')
    geometria = models.GeometryField(srid=4326)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    toponim_permission = models.CharField(max_length=200, null=True, blank=True)
    permission_recurs_edition = models.BooleanField(default=False)
    permission_toponim_edition = models.BooleanField(default=False)
    permission_tesaure_edition = models.BooleanField(default=False)
    permission_administrative = models.BooleanField(default=False)
    permission_filter_edition = models.BooleanField(default=False)


class Autor(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=pkgen)
    nom = models.CharField(max_length=500)

    def __str__(self):
        return '%s' % (self.nom)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


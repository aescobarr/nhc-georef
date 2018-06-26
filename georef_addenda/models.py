from django.db import models
from django.contrib.gis.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
#from georef.models import Toponim, Recursgeoref, Toponimversio, pkgen
from georef.tasks import pkgen
import djangoref.settings as conf
import os


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

    @property
    def is_admin(self):
        return self.permission_administrative

    @property
    def can_edit_recurs(self):
        return self.permission_recurs_edition

    @property
    def can_edit_toponim(self):
        return self.permission_toponim_edition

    @property
    def can_edit_tesaure(self):
        return self.permission_tesaure_edition

    @property
    def can_edit_filtre(self):
        return self.permission_filter_edition

class Autor(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=pkgen)
    nom = models.CharField(max_length=500)

    def __str__(self):
        return '%s' % (self.nom)


class HelpFile(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=pkgen)
    titol = models.TextField()
    h_file = models.FileField(upload_to=conf.LOCAL_DATAFILE_ROOT_DIRECTORY)
    created_on = models.DateField(auto_now_add=True)


@receiver(models.signals.post_delete, sender=HelpFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.h_file:
        if os.path.isfile(instance.h_file.path):
            os.remove(instance.h_file.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


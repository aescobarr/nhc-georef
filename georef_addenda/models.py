from django.db import models
from django.contrib.gis.db import models
from georef.models import Toponimversio
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from georef.models import Toponim

# Create your models here.
class GeometriaToponimVersio(models.Model):
    idversio = models.ForeignKey(Toponimversio, on_delete=models.CASCADE, db_column='idversio', blank=True, null=True, related_name='geometries')
    geometria = models.GeometryField(srid=4326)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    toponim_permission = models.CharField(max_length=200, null=True, blank=True)
    permission_recurs_edition = models.BooleanField(default=False)
    permission_toponim_edition = models.BooleanField(default=False)
    permission_tesaure_edition = models.BooleanField(default=False)
    permission_administrative = models.BooleanField(default=False)
    permission_filter_edition = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


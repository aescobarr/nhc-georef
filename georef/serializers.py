from rest_framework import serializers
from georef.models import Toponim, Tipustoponim, Filtrejson, Recursgeoref, Toponimversio, Paraulaclau, Capawms, \
    Capesrecurs, Qualificadorversio, Pais, Tipusrecursgeoref, Suport, Tipusunitats
from georef_addenda.models import Profile, Autor
from django.contrib.auth.models import User
import json


class TipusToponimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipustoponim
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Profile
        fields = '__all__'


class ToponimSearchSerializer(serializers.ModelSerializer):
    aquatic_str = serializers.ReadOnlyField()
    nom_str = serializers.ReadOnlyField()
    idtipustoponim = TipusToponimSerializer(required=True)
    coordenada_x_centroide = serializers.SerializerMethodField()
    coordenada_y_centroide = serializers.SerializerMethodField()
    precisio = serializers.SerializerMethodField()

    class Meta:
        model = Toponim
        fields = '__all__'

    def get_coordenada_x_centroide(self, obj):
        darrera_versio = obj.get_darrera_versio()
        if darrera_versio is None:
            return None
        else:
            return darrera_versio.get_coordenada_x_centroide

    def get_coordenada_y_centroide(self, obj):
        darrera_versio = obj.get_darrera_versio()
        if darrera_versio is None:
            return None
        else:
            return darrera_versio.get_coordenada_y_centroide

    def get_precisio(self, obj):
        darrera_versio = obj.get_darrera_versio()
        if darrera_versio is None:
            return None
        else:
            return darrera_versio.precisio_h

class ToponimSerializer(serializers.ModelSerializer):
    aquatic_str = serializers.ReadOnlyField()
    nom_str = serializers.ReadOnlyField()
    idtipustoponim = TipusToponimSerializer(required=True)
    editable = serializers.SerializerMethodField()

    class Meta:
        model = Toponim
        fields = '__all__'

    def get_editable(self, obj):
        user = self.context['request'].user
        if user.profile.toponim_permission == '1':
            return True
        if user.profile.toponim_permission in obj.denormalized_toponimtree:
            return True
        return False


class ToponimVersioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toponimversio
        fields = '__all__'


class FiltrejsonSerializer(serializers.ModelSerializer):
    description = serializers.ReadOnlyField()

    class Meta:
        model = Filtrejson
        #fields = '__all__'
        fields = ('idfiltre', 'json', 'modul', 'nomfiltre', 'description')


class RecursgeorefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recursgeoref
        fields = ('id', 'nom')


class TipusunitatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipusunitats
        fields = ('id', 'tipusunitat')


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ('id', 'nom')


class SuportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suport
        fields = ('id', 'nom')


class TipusrecursgeorefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipusrecursgeoref
        fields = ('id', 'nom')


class QualificadorversioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualificadorversio
        fields = ('id', 'qualificador')


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'nom')


class ParaulaClauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paraulaclau
        fields = ('id', 'paraula')


class CapawmsSerializer(serializers.ModelSerializer):

    visible = serializers.SerializerMethodField()

    class Meta:
        model = Capawms
        fields = ('id','baseurlservidor','name','label','minx','maxx','miny','maxy','boundary','visible')

    def get_visible(self, obj):
        user = self.context['request'].user
        if len(user.prefswms.all()) > 0:
            prefs = user.prefswms.first()
            p_json = json.loads(prefs.prefscapesjson)
            for elem in p_json:
                if elem['id'] == obj.id:
                    return True
        return False
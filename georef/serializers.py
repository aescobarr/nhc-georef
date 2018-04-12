from rest_framework import serializers
from georef.models import Toponim, Tipustoponim, Filtrejson, Recursgeoref, Toponimversio, Paraulaclau, Capawms, Capesrecurs
from georef_addenda.models import Profile, Autor
from django.contrib.auth.models import User


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


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'nom')

class ParaulaClauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paraulaclau
        fields = ('id', 'paraula')


class CapawmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capawms
        fields = '__all__'
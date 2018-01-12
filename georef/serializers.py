from rest_framework import serializers
from georef.models import Toponim, Tipustoponim, Filtrejson, Recursgeoref, Toponimversio


class TipusToponimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipustoponim
        fields = '__all__'


class ToponimSerializer(serializers.ModelSerializer):
    aquatic_str = serializers.ReadOnlyField()
    nom_str = serializers.ReadOnlyField()
    idtipustoponim = TipusToponimSerializer(required=True)

    class Meta:
        model = Toponim
        fields = '__all__'


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
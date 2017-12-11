from rest_framework import serializers
from georef.models import Toponim, Tipustoponim, Filtrejson


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

class FiltrejsonSerializer(serializers.ModelSerializer):
    description = serializers.ReadOnlyField()
    class Meta:
        model = Filtrejson
        #fields = '__all__'
        fields = ('idfiltre', 'json', 'modul', 'nomfiltre', 'description')
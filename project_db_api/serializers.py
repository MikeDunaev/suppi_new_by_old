from rest_framework import serializers
from calculations.models import *


class Main_analytic_serializer(serializers.ModelSerializer):
    class Meta:
        model = Main_analytic
        fields = '__all__'


class Supplies_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = Supplies_info
        fields = '__all__'


class ABC_serializer(serializers.ModelSerializer):
    class Meta:
        model = ABC
        fields = '__all__'
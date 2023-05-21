from rest_framework import serializers

from rec_rest.models import Table


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'schema']


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

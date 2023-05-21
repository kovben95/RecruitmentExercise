from django.shortcuts import render
from rest_framework import viewsets, permissions

from rec_rest.models import Table
from rec_rest.serializers import TableSerializer, DataSerializer


# Create your views here.
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('-created')
    serializer_class = TableSerializer


class DataViewSet(viewsets.ModelViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = {}

    def get_model(self, key):
        if key not in self._model:
            self._model[key] = Table.objects.get(id=key).ModelClass
        return self._model[key]

    def get_queryset(self):
        model_name = self.kwargs.get('id')
        model = self.get_model(model_name)
        return model.objects.all()

    def get_serializer_class(self):
        model_name = self.kwargs.get('id')
        DataSerializer.Meta.model = self.get_model(model_name)
        return DataSerializer

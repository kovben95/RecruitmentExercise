from django.urls import path, include
from rest_framework import routers

from rec_rest.views import TableViewSet, DataViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'table', TableViewSet, basename='Table')
router.register(r'table/(?P<id>\w+)/row', DataViewSet, basename='Data')
router.register(r'table/(?P<id>\w+)/rows', DataViewSet, basename='Data')

urlpatterns = [
    path('', include(router.urls)),
]

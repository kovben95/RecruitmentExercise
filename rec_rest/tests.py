from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from rec_rest.models import Table


class PostApiTableTests(APITestCase):
    def test_create_account(self):
        data = {
            "id": 1,
            "schema": {
                "name": "str",
                "age": "int",
                "male": "bool",
            }
        }
        response = self.client.post("/api/table/", data, format="json")
        content = json.loads(response.content)
        idd = content["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.get(id=idd).id, idd)

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from rec_rest.models import Table


class PostApiTableTests(APITestCase):

    def test_create_schema_add_data(self):
        response = self.client.post("/api/table", {
            "schema": {
                "name": "str",
                "age": "int",
                "male": "bool",
            }
        }, format="json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Table.objects.filter(id=content["id"]).exists())

        self.client.post("/api/table/1/row", {
            "name": "User",
            "age": 27,
            "male": False
        })

        response = self.client.put("/api/table/1", {
            "schema": {
                "name": "str",
                "age": "int",
                "gender": "int",
                "shirt_size": "str"
            }
        }, format="json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Table.objects.filter(id=content["id"]).exists())

        self.client.post("/api/table/1/row", {
            "name": "User",
            "age": 27,
            "gender": 1,
            "shirt_size": "m"
        })

        result = self.client.get("/api/table/1/rows")
        content = json.loads(result.content)
        self.assertEqual(content, [{"id": 1, "age": 27, "name": "User", "gender": 0, "shirt_size": ""},
                                   {"id": 2, "age": 27, "name": "User", "gender": 1, "shirt_size": "m"}])

#    def test_invalid_db_migration(self):
        response = self.client.post("/api/table", {
            "schema": {
                "name": "str",
                "age": "int",
                "male": "bool",
            }
        }, format="json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Table.objects.filter(id=content["id"]).exists())

        response = self.client.put("/api/table/2", {
            "schema": {
                "name": "str",
                "age": "bool",
                "gender": "int",
                "shirt_size": "str"
            }
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#    def test_db_field_name_error(self):
        response = self.client.post("/api/table", {
            "schema": {
                "name_": "str",
                "age": "int",
                "male": "bool",
            }
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Table.objects.count(), 2)

        response = self.client.post("/api/table", {
            "schema": {
                "name": "str",
                "ag__e": "int",
                "male": "bool",
            }
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Table.objects.count(), 2)

        response = self.client.post("/api/table", {
            "schema": {
                "name": "str",
                "age": "int",
                "1male": "bool",
            }
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Table.objects.count(), 2)

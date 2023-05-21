from django.http import JsonResponse
from rest_framework.views import exception_handler


class InputDataFormatException(Exception):

    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        return f'Input data format exception: {self.message}'

    def __repr__(self) -> str:
        return str(self)


def exc_handler(exc, context):
    return JsonResponse({
        'error': str(exc),
    }, status=400 if type(exc) is InputDataFormatException else 500)

from django.apps import AppConfig
from django.db import models, transaction, connection
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

from rec_rest.exc_handler import InputDataFormatException
from rec_rest.tools import verify_schema


def type_name_to_column(name: str, field_name: str):
    """
    Convert type name to column
    :param name: str representing col type
    :param field_name: the name of field for verbose error message
    :return:
    """
    if name not in ['str', 'int', 'bool']:
        raise InputDataFormatException(f'Type of field {field_name} must be either "str", "int", or "bool", not {name}')
    if name == 'str':
        return models.TextField(default='')
    if name == 'int':
        return models.IntegerField(default=0)
    if name == 'bool':
        return models.BooleanField(default=False)


types = {}


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    schema = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_schema = self.schema if self.id is not None else None

    def get_model_class(self, old=False):
        """
        create a dynamic model from the class and return it
        :param old: bool: use old model or no
        :return: the dynamic model class
        """
        schem = {k: type_name_to_column(v, k) for k, v in (self.old_schema if old else self.schema).items()}
        schem['__module__'] = f'rec_rest.models'
        return type(f'Class_{self.id}', (models.Model,), schem)

    def __str__(self):
        return f'Table {self.id}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        verify_schema(schema=self.schema)
        with transaction.atomic():
            super().save(force_insert, force_update, using, update_fields)
            schema_editor: DatabaseSchemaEditor
            with connection.schema_editor() as schema_editor:
                if self.old_schema is None:
                    mc = self.get_model_class(old=False)
                    schema_editor.create_model(mc)
                else:
                    mc = self.get_model_class(old=True)
                    added = self.schema.keys() - self.old_schema.keys()
                    removed = self.old_schema.keys() - self.schema.keys()
                    for r in removed:
                        field = [a for a in mc._meta.get_fields() if a.attname == r][0]
                        schema_editor.remove_field(mc, field)
                    for a in added:
                        f = type_name_to_column(self.schema[a], a)
                        f.column = a
                        schema_editor.add_field(mc, f)
                    typeval = set(self.old_schema.keys()) & set(self.schema.keys())
                    for t in typeval:
                        if self.old_schema[t] != self.schema[t]:
                            raise InputDataFormatException(f'Type changes are not permitted for existing col: {t}: '
                                                           f'{self.old_schema[t]} -> {self.schema[t]}')

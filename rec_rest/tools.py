from rec_rest.exc_handler import InputDataFormatException


def verify_schema(schema: dict):
    if type(schema) is not dict:
        raise InputDataFormatException('Schema must be a JSON dictionary such as: {"column": "str|int|bool"}')
    for col_name in schema.keys():
        if len(col_name) == 0:
            raise InputDataFormatException(f'Column name should be at least one character, got: {col_name}')
        if '__' in col_name:
            raise InputDataFormatException(f'__ is not allowed in column name, got {col_name}')
        if col_name[-1] == '_':
            raise InputDataFormatException(f'_ is not as last character of column name, got {col_name}')
        if not str(col_name[0]).isalpha():
            raise InputDataFormatException(f'First letter of column should be a letter, got: {col_name}')
        if not col_name.replace('_', '').isalnum():
            raise InputDataFormatException(f'Column name allows alphanumeric characters and _, got: {col_name}')

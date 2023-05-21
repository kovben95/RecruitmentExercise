# Django Dynamic Model API

Project for recruitment exercise.

## How to run?

### Database

To start the database run the `run_db.sh` file.
The script requires Docker to be installed and was tested on Mac.

Make sure to test the database connection with the mock username and password, before starting the Django app.

### Django app

Install requirements

```
pip install -r requirements.txt
```

Run tests:

```
./manage.py test
```

Run dev server:

```
./manage.py migrate
./manage.py runserver
```


### Test requests

```
POST http://127.0.0.1:8000/api/table
Content-Type: application/json
Accept: application/json

{
    "schema": {
        "name": "str",
        "age": "int",
        "male": "bool"
    }
}
```

```
GET http://127.0.0.1:8000/api/table/1/rows
Content-Type: application/json
Accept: application/json
```

```
POST http://127.0.0.1:8000/api/table/1/row
Content-Type: application/json
Accept: application/json

{
    "name": "User",
    "age": 27,
    "male": false
}
```

```
GET http://127.0.0.1:8000/api/table/1/rows
Content-Type: application/json
Accept: application/json
```

```
PUT http://127.0.0.1:8000/api/table/1
Content-Type: application/json
Accept: application/json

{
    "schema": {
        "name": "str",
        "age": "int",
        "gender": "int",
        "shirt_size": "str"
    }
}
```

```
POST http://127.0.0.1:8000/api/table/1/row
Content-Type: application/json
Accept: application/json

{
    "name": "User",
    "age": 27,
    "gender": 1,
    "shirt_size": "m"
}
```

```
GET http://127.0.0.1:8000/api/table/1/rows
Content-Type: application/json
Accept: application/json
```
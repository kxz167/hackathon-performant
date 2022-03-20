# Performant Backend

The backend server is what will link the TD Ameritrade API with the Angular frontend, as well as perform python scripts in order to process price history and calculate performance metrics.

## Dependencies:

This backend requires the following packages:

- flask
- requests
- psycopg2

As well as other smaller libraries. Because of the time crunch, these can really be found under `/backend/performant_api/__init__.py`

## Framework:

I intend to use Flask as a simple light backend server. I have never used flask before and will be looking at the following tutorials:

- [Flask Tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
    - Up until "database" provides flask setup and running.
- [Flask Rest API Tutorial](https://pythonbasics.org/flask-rest-api/)
    - Takes over, in order to create the api.
- [PostgreSQL Python](https://www.postgresqltutorial.com/postgresql-python/)
    - Used for learning about postgresql access in python

## Launching the server

In order to run the application form Powershell, be in the `backend` directory. Then run:

```
$env:FLASK_APP = "performant_api"
$env:FLASK_ENV = "development"
flask run
```

The server will then be running on [`http://127.0.0.1:5000`](http://127.0.0.1:5000).

Alternatively, you can also select the port using:
```
flask run --port <port#>
```

But note that if you do use a different port, you will need to make the requesite changes in the Angular environment files.

## Secrets:

For the current api backend, secrets have been protected. In order for your project to work, create a file named `secrets.py` inside `/backend/performant_api`

Then, define the following:
- `connection_string = "<string with connection options>"`
    - ex: `"dbname=database_name user=login_user password=secure_pw host=server_address port=server_port"`
- `tda_clientid = "<TDA Client ID from API>"`
    - This will require a devloper and TDA trading account as well as a registered app.

Once the file has been created, you should be able to easily and simply run the server.

## Files:

The majority of the important python files are the following listed under `performant_api`:
- __init__.py
    - This is where all of the API endpoints are defined. This might be bad, but it makes life very easy.
- tda_requester.py
    - This is a python module that will handle all of the API querying to receive TDA candlesticks.
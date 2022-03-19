# Backend

The backend server is what will link the TD Ameritrade API with the Angular frontend, as well as perform python scripts in order to process price history and calculate performance metrics.

## Framework:

I intend to use Flask as a simple light backend server. I have never used flask before and will be looking at the following tutorials:

- [Flask Tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
- [Flask Rest API Tutorial](https://pythonbasics.org/flask-rest-api/)

## Running

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
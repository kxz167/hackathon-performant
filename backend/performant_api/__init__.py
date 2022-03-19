#Secrets:
from .secrets import connection_string, tda_clientid

#Postgres Driver
import psycopg2

#Flask
from flask import Flask

#API Requests
import requests

global conn

def create_app(test_config=None):
    #Initialize the DB:
    conn = psycopg2.connect(connection_string)

    #Setup flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', #'dev' should be replaced with a value at launch
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') # WE DO NOT NEED A DATABASE
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Instance path is only required for SQLite Database
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # Define routes
    @app.route('/hello')
    def hello():

        print("====== Database stuff ======")
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        print("============================")

        print("====== Requests stuff ======")
        response = requests.get("https://api.tdameritrade.com/v1/marketdata/TSLA/pricehistory?apikey=%s&periodType=month&period=1&frequencyType=daily&frequency=1" % tda_clientid)
        print(response.json())
        print("============================")
        
        
        return response.json()
    
    

    return app
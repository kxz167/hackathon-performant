#Secrets:
from .secrets import connection_string

#Postgres Driver
import psycopg2

#Flask
from flask import Flask, request
from flask_cors import CORS, cross_origin

import json

#API Requests
from .tda_requester import price_history
import requests

global conn

def create_app(test_config=None):
    #Initialize the DB:
    conn = psycopg2.connect(connection_string)

    #Setup flask
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev', #'dev' should be replaced with a value at launch
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') # WE DO NOT NEED A DATABASE
    )

    app.config['CORS_HEADERS'] = 'Content-type'

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
        # response = requests.get(price_history())
        # print(response.json())
        candles = price_history()
        print(len(candles))
        print("============================")
        
        
        return {"candles": candles}
    
    @app.route('/account/get-accounts')
    @cross_origin()
    def get_accounts():
        cur = conn.cursor()
        cur.execute('SELECT account.uuid, name, description, sum(account_transaction.amount) FROM account JOIN account_transaction ON account.uuid=account_transaction.account_uuid GROUP BY account.uuid;')
        accounts = cur.fetchall()
        # print(acconts)
        return {"accounts": accounts}

    @app.route('/account/fund-account', methods=['POST'])
    @cross_origin()
    def fund_account():
        record = json.loads(request.data)
        cur = conn.cursor()
        cur.execute(f'INSERT INTO account_transaction (account_uuid, amount, date) VALUES (\'{record["account"]}\',{record["amount"]}, \'{record["date"]}\');')
        conn.commit()
        print(record)
        return {"status": "good"}

    @app.route('/position/make-transaction', methods=['POST'])
    @cross_origin()
    def make_transaction():
        record = json.loads(request.data)
        cur = conn.cursor()
        cur.execute(f'INSERT INTO position_transaction (account_uuid, quantity, ticker, date, price) VALUES (\'{record["account"]}\', {record["quantity"]}, \'{record["ticker"]}\', \'{record["date"]}\', {record["price"]});')
        conn.commit()
        # print(record)
        return {"status": "good"}

    return app
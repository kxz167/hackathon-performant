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

#Dates:
from datetime import date as sys_date
import time

#TEMPORARY TESTING
from decimal import Decimal
global DAY_IN_MILLI
DAY_IN_MILLI = Decimal('86400000')

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
        cur.execute(f'INSERT INTO position_transaction (account_uuid, quantity, ticker, date, price) VALUES (\'{record["account"]}\', {record["quantity"]}, \'{record["ticker"]}\', \'{record["date"]}\', {record["price"]}) RETURNING ticker, extract(epoch from date) * 1000 as date;')
        conn.commit()
        results = cur.fetchall()

        print(results)

        # update_pos_history(*results[0])
        update_pos_history(*("AAPL",Decimal('1646784000000')))

        # print(record)
        return {"status": "good"}

    @app.route('/position/get-transactions')
    @cross_origin()
    def get_transactions():
        cur = conn.cursor()
        cur.execute('SELECT ticker, jsonb_agg(to_jsonb(position_transaction.*) - \'{ticker, account_uuid}\'::text[] ORDER BY date) FROM position_transaction GROUP BY ticker;')
        transactions = cur.fetchall()
        # print(acconts)
        return {"transactions": transactions}

    
    @app.route('/position/test-calc')
    @cross_origin()
    def test_calc():
        update_pos_history(*("AAPL",Decimal('1646784000000'), "2022-3-9"))
        return 'testing'


    # HELPER FUNCTIONS:
    # THERE IS 86400000 miliseconds in 24 hours
    def update_pos_history(ticker, date, date_text):
        # GET INFO FROM TDA:
        # date=postgres_time_to_tda(date)
        ticker_history = price_history(ticker, postgres_time_to_tda(date)-DAY_IN_MILLI)
        cur = conn.cursor()
        cur.execute(f'SELECT extract(epoch from date)*1000 as date, quantity FROM position_transaction WHERE ticker = \'{ticker}\' AND date >= \'{date_text}\' ORDER BY date;')
        quantities = cur.fetchall()
        print(f"DATE:{date}, TDA DATE: {postgres_time_to_tda(date)}, QUERIED DATE: {postgres_time_to_tda(date)-DAY_IN_MILLI}")
        updated_history = []
        for i in range(1,len(ticker_history[1:])):
            print(i)
            candle = ticker_history[i]
            print(candle)
            updated_history.append(candle["close"])

        print(updated_history)

        print(f'Ticker: {ticker}, Date {date}')
        print(sys_date.today())
        # print(time.time() * 1000 - DAY_IN_MILLI)
        # print(sys_date.today().utcfromtimestamp(0))

    def tda_time_to_postgres(date):
        return date - 21600000

    def postgres_time_to_tda(date):
        return date + 21600000

    return app
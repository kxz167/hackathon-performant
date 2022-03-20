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
        cur.execute(f'INSERT INTO position_transaction (account_uuid, quantity, ticker, date, price) VALUES (\'{record["account"]}\', {record["quantity"]}, \'{record["ticker"]}\', \'{record["date"]}\', {record["price"]}) RETURNING account_uuid, ticker, extract(epoch from date) * 1000 as date, date as date_text;')
        conn.commit()
        results = cur.fetchone()

        print(results)

        # update_pos_history(*results[0])
        update_pos_history(*results)

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
        update_pos_history(*("3d23e8c1-71f1-48f8-a323-60fd159f3c37","AAPL",Decimal('1646784000000'), "2022-3-9"))
        return 'testing'


    # HELPER FUNCTIONS:
    # THERE IS 86400000 miliseconds in 24 hours
    def update_pos_history(account_uuid, ticker, date, date_text):
        # GET INFO FROM TDA:
        ticker_history = price_history(ticker, postgres_time_to_tda(date)-DAY_IN_MILLI)
        # Get quantities from DB
        cur = conn.cursor()
        cur.execute(f'SELECT extract(epoch from date)*1000 as date, quantity FROM position_transaction WHERE ticker = \'{ticker}\' ORDER BY date;')
        quantities = cur.fetchall()
        #Quantity tracker:
        qt = Quantity_Tracker(quantities)

        print(f"Ticker: {ticker}, DATE:{date}, TDA DATE: {postgres_time_to_tda(date)}, QUERIED DATE: {postgres_time_to_tda(date)-DAY_IN_MILLI}")
        print(quantities)

        # Get the previous history:
        cur = conn.cursor()
        cur.execute(f"SELECT pl::NUMERIC, plp, avg_price FROM position_transaction_history WHERE date < \'{date_text}\' ORDER BY date DESC LIMIT 1;")
        prev_history = cur.fetchone()
        print(prev_history)

        #Run through all the necessary days:
        updated_history = []
        prev_pl = 0
        if(prev_history is not None):
           prev_pl = float(prev_history[0])
        print(ticker_history[0])
        for i in range(1,len(ticker_history[1:])):
            print("==============")
            # print(i)
            candle = ticker_history[i]

            prev_close = ticker_history[i-1]["close"]
            curr_close = candle["close"]
            
            curr_quantity = qt.get_quantity(candle["datetime"])
            # curr_quantity = qt.get_quantity(tda_time_to_postgres(candle["datetime"]))
            
            curr_pl = (curr_close - prev_close) * curr_quantity + prev_pl
            prev_pl = curr_pl

            curr_pl_per = curr_pl / (curr_close * curr_quantity)

            curr_date = sys_date.fromtimestamp(candle["datetime"]/1000)
            # print(type(candle["datetime"]))
            # print(sys_date.fromtimestamp(candle["datetime"]/1000))

            tot_val = curr_close * curr_quantity

            print(f"DATE: {curr_date}, Quantity: {curr_quantity}, PL: {curr_pl}, PL%: {curr_pl_per}")

            cur = conn.cursor()
            cur.execute(f"INSERT INTO position_transaction_history (account_uuid, date, ticker, quantity, pl, plp, tot_value) VALUES (\'{account_uuid}\', \'{curr_date}\', \'{ticker}\', {curr_quantity}, {curr_pl}, {curr_pl_per}, {tot_val}) ON CONFLICT ON CONSTRAINT position_transaction_history_pkey DO UPDATE SET quantity = EXCLUDED.quantity, pl = EXCLUDED.pl, plp = EXCLUDED.plp, tot_value = EXCLUDED.tot_value;")
            conn.commit()

            print(candle)
            updated_history.append(candle["close"])

        print(updated_history)

        # print(sys_date.today())
        # print(time.time() * 1000 - DAY_IN_MILLI)
        # print(sys_date.today().utcfromtimestamp(0))

    def tda_time_to_postgres(date):
        return date - 21600000

    def postgres_time_to_tda(date):
        return date + 21600000

    @app.route('/position/graph-data', methods=['POST'] )
    @cross_origin()
    def position_graph_data():
        ticker = json.loads(request.data)["ticker"]
        print(ticker)
        cur = conn.cursor()
        cur.execute(f"SELECT ticker, jsonb_agg((SELECT x FROM (SELECT date AS name, pl::Numeric AS value ORDER BY date) AS x)) AS pl,jsonb_agg((SELECT x FROM (SELECT date AS name, plp AS value ORDER BY date) AS x)) AS plp,jsonb_agg((SELECT x FROM (SELECT date AS name, quantity AS value ORDER BY date) AS x)) AS quantity FROM position_transaction_history WHERE ticker = \'{ticker}\' GROUP BY ticker;")
        gdata = cur.fetchone()
        # print(gdata)
        # print(acconts)
        return {"graphdata": gdata}

    @app.route('/position/ticks')
    @cross_origin()
    def position_ticks():
        cur = conn.cursor()
        cur.execute("SELECT ticker FROM position_transaction_history GROUP BY ticker;")
        tickers = cur.fetchall()
        # print(acconts)
        return {"tickers": tickers}

    # =================================================
    # ACCOUNTS
    @app.route('/account/summary/dep-bal')
    @cross_origin()
    def account_summary_dep_bal():
        cur = conn.cursor()
        cur.execute("SELECT jsonb_agg((SELECT x FROM (SELECT date as name, amount as value ORDER BY date) as x)) FROM account_transaction WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37';")
        summary = cur.fetchone()
        return {"summary": summary}

    @app.route('/account/summary/inv-val')
    @cross_origin()
    def account_summary_inv_val():
        cur = conn.cursor()
        cur.execute("SELECT jsonb_agg(json_build_object) FROM (SELECT json_build_object('name', date, 'value', sum(tot_value)) FROM position_transaction_history WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY account_uuid, date ORDER BY date) as x;")
        summary = cur.fetchone()
        return {"summary": summary}

    @app.route('/account/summary/avail-funds')
    @cross_origin()
    def account_summary_avail_funds():
        cur = conn.cursor()
        cur.execute("SELECT jsonb_agg(json_build_object) FROM (SELECT json_build_object ('value', value, 'name', name) FROM(SELECT account_uuid, amount as value, date as name FROM account_transaction UNION SELECT account_uuid, -1 * (price*quantity) as value, date as name FROM position_transaction) as a WHERE a.account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' ORDER BY name ) as x;")
        summary = cur.fetchone()
        return {"summary": summary}

    @app.route('/account/summary/overall-pl')
    @cross_origin()
    def account_summary_overall_pl():
        cur = conn.cursor()
        cur.execute("SELECT jsonb_agg(json_build_object) FROM (SELECT json_build_object('name',date, 'value' , sum(pl)) FROM position_transaction_history WHERE account_uuid = '3d23e8c1-71f1-48f8-a323-60fd159f3c37' GROUP BY date, account_uuid ORDER BY date ) as x;")
        summary = cur.fetchone()
        return {"summary": summary}

    return app

class Quantity_Tracker:
    def __init__(self, quantities):
        print(quantities)
        self.quantities = quantities
        self.index = -1

        self.prev_date = quantities[0][0]
        # self.prev_date = 0
        self.quantity = quantities[0][1]
        # self.quantity = 0

    # This was not working
    def get_quantity2(self, date):
        print("GET QUANTITY", self.prev_date, date, self.prev_date - date, self.quantities, self.quantity, self.index)
        while(self.prev_date < date and self.index < len(self.quantities)):
            self.index += 1
            self.quantity += self.quantities[self.index][1]
            self.prev_date = self.quantities[self.index][0]

            print(self.quantity, self.prev_date, self.index)

        return self.quantity

    # And this sucks but it works.
    def get_quantity(self, date):
        quantity = 0
        print("GQ: ", date, self.quantities)
        for tx in self.quantities:
            if(tx[0] <= date):
                quantity += tx[1]
        
        return quantity
        


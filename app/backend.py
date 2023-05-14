from flask import Flask, jsonify, send_file, request
import mysql.connector
import boto3
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/data')
def get_data():
    # Connect to the MySQL DB instance
    cnx = mysql.connector.connect(user='admin', password='Arby_13245',
                                   host='arbydb.camodfosky75.ap-southeast-1.rds.amazonaws.com', database='ARBY')
    
    # Execute an SQL query to retrieve data from the table
    cursor = cnx.cursor()
    query = 'SELECT * FROM Tokens'
    cursor.execute(query)
    data = cursor.fetchall()
    
    # Close the database connection
    cnx.close()
    print(data)
    
    # Return the retrieved data as a JSON response
    return jsonify(data)
    
# Access Binance API
BASE_URL = 'https://api.binance.com/api/v3'
ENDPOINTS = {
    'klines': '/klines',
    'ticker_price': '/ticker/price',
    'ticker_book': '/ticker/bookTicker'
}


@app.route('/api/ticker/book')
def get_ticker_book():

    symbol_list = ['BTCUSDT','ETHUSDT','BNBUSDT','BTCTUSD','PEPEUSDT']
    response_list = []
    for symbol in symbol_list :
        params = {'symbol': symbol}
        response = requests.get(BASE_URL + ENDPOINTS['ticker_book'], params=params)
        response_data = response.json()
        response_list.append(response_data)
    return jsonify(rows=response_list)
    
@app.route('/')
def home():
    s3 = boto3.client('s3')
    s3.download_file('arbybucket', 'index.html', '/tmp/index.html')
    return send_file('/tmp/index.html', mimetype='text/html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    



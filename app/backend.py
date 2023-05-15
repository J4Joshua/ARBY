from flask import Flask, jsonify, send_file, request
import mysql.connector
import boto3
import requests
import json
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


# Connect to the MySQL DB instance
cnx = mysql.connector.connect(user='admin', password='Arby_13245',
                               host='arbydb.camodfosky75.ap-southeast-1.rds.amazonaws.com', database='ARBY')
# Execute an SQL query to retrieve data from the table
cursor = cnx.cursor()


# Add User to database
def add_user(username):
    query = "INSERT INTO `ARBY`.`users` (`Username`) VALUES (%s)"
    cursor.execute(query, (username,))
    # ticker = json.dumps(['BTCUSDT'])
    # cursor.execute("INSERT INTO `ARBY`.`users` (`Tickers`) VALUES CAST(%s AS BLOB))", (ticker,))
    cnx.commit()
    return



@app.route('/check_user', methods=['POST'])
def check_user():
    # Get the username from the frontend
    content = request.json
    username = content['username']
    method = content['method']
    
    # Query the MySQL database to check if User already exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user_data = cursor.fetchall()
    
    # Add user if doesn't yet exist
    if method == 'register':
        if not user_data:
            add_user(username)
            return jsonify({'status': 'success', 'message': 'User added'})
        else:
            return jsonify({'status': 'error', 'message': 'Already registered'})
    else:
        if not user_data:
            return jsonify({'status': 'error', 'message': 'User not registered'})
        else:
            return jsonify({'status': 'success', 'message': 'Success', 'user_data': user_data})



# Access Binance API
BASE_URL = 'https://api.binance.com/api/v3'
ENDPOINTS = {
    'klines': '/klines',
    'ticker_price': '/ticker/price',
    'ticker_book': '/ticker/bookTicker'
}
def get_ticker_book(symbol_list):
    response_list = []
    for symbol in symbol_list :
        
        params = {'symbol': symbol}
        response = requests.get(BASE_URL + ENDPOINTS['ticker_book'], params=params)
        response_data = response.json()
        print(response_data)
        if 'symbol' not in response_data:
            return jsonify(status='error')
        response_list.append(response_data)
    return jsonify(rows=response_list,status='success')
symbol_list = ['BTCUSDT']

@app.route('/getdata')
def get_pair():
    return get_ticker_book(symbol_list)

@app.route('/addpair', methods=['POST'])
def add_pair():
    content = request.json
    pairname = content['pairname']
    symbol_list.append(pairname)
    return get_ticker_book(symbol_list)

@app.route('/removepair', methods=['POST'])
def remove_pair():
    content = request.json
    pairname = content['pairname']
    symbol_list.remove(pairname)
    return get_ticker_book(symbol_list)
    


@app.route('/')
def home():
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    



from flask import Flask, jsonify, send_file, request
import mysql.connector
import boto3
import requests
import json
import hashlib
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache


app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret" 
jwt = JWTManager(app)


cnx = mysql.connector.connect(user='admin', password='admin123', host='arbydb.camodfosky75.ap-southeast-1.rds.amazonaws.com', database='ARBY')
cursor = cnx.cursor()

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)


#------------------------------------------USERDATA-----------------------------------------------------------
# Add User to database
def add_user(username, password):
    query = "INSERT INTO `ARBY`.`users` (`Username`,`Password`) VALUES (%s,%s)"
    cursor.execute(query, (username, password))
    query = "INSERT INTO `ARBY`.`tickers` (`iduser`, `ticker`) VALUES ((SELECT `idLogin` FROM `ARBY`.`users` WHERE `Username` = %s), 'BTCUSDT')"
    cursor.execute(query, (username,))
    cnx.commit()
    return

@app.route('/check_user', methods=['POST'])
def check_user():
    content = request.json
    username = content['username']
    password = content['password']
    method = content['method']
    
    # Query the MySQL database to check if User already exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user_data = cursor.fetchall()
    
    # Add user if doesn't yet exist
    if method == 'register':
        if not user_data:
            add_user(username,password)
            return jsonify({'status': 'success', 'message': 'User added'})
        else:
            return jsonify({'status': 'error', 'message': 'Already registered'})
    else:
        if not user_data:
            return jsonify({'status': 'error', 'message': 'User not registered'})
        else:
            user_data = user_data[0]
            userid = user_data[0]
            user_password = user_data[2]
            if user_password == password:
                access_token = create_access_token(identity=userid)
                return jsonify({'status': 'success', 'jwtToken': access_token, 'message': 'Logged in'})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid credentials'})



#------------------------------------------TICKERDATA-----------------------------------------------------------
# Access Binance API
BASE_URL = 'https://api.binance.com/api/v3'
ENDPOINTS = {
    'klines': '/klines',
    'ticker_price': '/ticker/price',
    'ticker_book': '/ticker/bookTicker'
}

def get_ticker_book(symbol_list):
    response_list = []
    for symbol in symbol_list:
        cache_key = f'ticker_book_{symbol}'
        response_data = cache.get(cache_key)
        if response_data is None:
            params = {'symbol': symbol}
            response = requests.get(BASE_URL + ENDPOINTS['ticker_book'], params=params)
            response_data = response.json()
            if 'symbol' not in response_data:
                return {'status': 'error'}
            cache.set(cache_key, response_data, timeout=60)
            print('cached')
        response_list.append(response_data)
    return response_list

@app.route('/getdata')
@jwt_required()
def get_pair():
    current_userid = get_jwt_identity()
    query = "SELECT `ticker` FROM `ARBY`.`tickers` WHERE `iduser` = %s"
    cursor.execute(query, (current_userid,))
    result = cursor.fetchall()
    return jsonify(rows=get_ticker_book(result),status='success')

@app.route('/addpair', methods=['POST'])
@jwt_required()
def add_pair():
    current_userid = get_jwt_identity()
    content = request.json
    pairname = content['pairname']
    query = "INSERT INTO `ARBY`.`tickers` (`iduser`, `ticker`) VALUES (%s, %s)"
    cursor.execute(query, (current_userid, pairname))
    cnx.commit()
    return get_pair()

@app.route('/removepair', methods=['POST'])
@jwt_required()
def remove_pair():
    current_userid = get_jwt_identity()
    content = request.json
    pairname = content['pairname']
    query = "DELETE FROM `ARBY`.`tickers` WHERE `iduser` = %s AND `ticker` = %s"
    cursor.execute(query, (current_userid, pairname))
    cnx.commit()
    return get_pair()
    


@app.route('/')
def home():
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    



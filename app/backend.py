from flask import Flask, jsonify, send_file
import mysql.connector
import boto3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/data')
def get_data():
    # Listen for requests


    
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
    
@app.route('/')
def home():
    s3 = boto3.client('s3')
    s3.download_file('arbybucket', 'index.html', '/tmp/index.html')
    return send_file('/tmp/index.html', mimetype='text/html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
    
    



from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/data')
print("hello")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



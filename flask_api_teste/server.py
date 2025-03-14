from flask import Flask, jsonify
from flask_cors import CORS
import random
import mysql.connector
import datetime 



app=Flask(__name__) 


CORS(app)

def create_connection():
    return mysql.connector.connect (
        host="localhost",
        user="root",
        password="123456",
        database="dados"
    )

def get_sensor_data():
    data ={
        "data": datetime.datetime.now(),
        "temperatura":round(random.uniform(20,80),2),
        "umidade":round(random.uniform(30,600),2),
        "pressao":round(random.uniform(900,1100),2),
        "gas":round(random.uniform(400,1000),2),
        "agua":round(random.uniform(600,800),2),
        "data": datetime.datetime.now()
    }

    insert_sensor_data(data)

    return data

def insert_sensor_data(data):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO sensores(umidade,pressao,temperatura,gas,agua,data) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['umidade'],data['pressao'],data['temperatura'],data['gas'],data['agua'],data['data']))

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


@app.route('/sensores',methods=['GET'])
def sensores():
    return jsonify(get_sensor_data())

if __name__=='__main__':
    app.run(debug=True)
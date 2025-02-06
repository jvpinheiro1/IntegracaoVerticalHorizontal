from flask import Flask, jsonify
from flask_cors import CORS
import random


#cria aplicação flask
app=Flask(__name__) 

#Habilita cors para permitir a requisição do javascript no servidor flask
CORS(app)

def get_sensor_data():
    return{
        #gerar valores aleatorios
        "temperatura":round(random.uniform(20,80),2),
        "umidade":round(random.uniform(30,90),2),
        "pressao":round(random.uniform(900,1100),2)
    }

#define a rota da API que responderá com os dados dos sensores em JSON
@app.route('/sensores',methods=['GET'])#A rota '/sensores' responde  apenas a requisicao GET
def sensores():
    return jsonify(get_sensor_data())#retorna os dados simulados em JSON

#executa o servidor flask diretamente
if __name__=='__main__':
    app.run(debug=True)#inicia o servidor em modo de depuração 
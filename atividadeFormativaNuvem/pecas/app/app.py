from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

componentes = []

@app.route('/entrada', methods=['POST'])
def registrar_entrada():
    data = request.json
    componente = {
        "id": str(uuid.uuid4()),
        "codigo": data['codigo'],
        "descricao": data['descricao'],
        "vin": data['vin'],  # Veículo em que a peça foi usada
        "data_entrada": data.get('data_entrada')
    }
    componentes.append(componente)
    return jsonify({"mensagem": "Componente registrado com sucesso", "componente": componente}), 201

@app.route('/entrada', methods=['GET'])
def listar_entradas():
    return jsonify(componentes)

@app.route('/entrada/<vin>', methods=['GET'])
def listar_por_vin(vin):
    resultado = [c for c in componentes if c['vin'] == vin]
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

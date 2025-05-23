from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

pecas_usadas = []

@app.route('/entrada', methods=['POST'])
def registrar_entrada():
    dados = request.get_json()
    peca = {
        'id': str(uuid.uuid4()),
        'codigo': dados['codigo'],
        'descricao': dados['descricao'],
        'vin': dados['vin']
    }
    pecas_usadas.append(peca)
    return jsonify(peca), 201

@app.route('/rastreio/<vin>', methods=['GET'])
def rastrear_pecas(vin):
    usadas = [p for p in pecas_usadas if p['vin'] == vin]
    return jsonify(usadas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

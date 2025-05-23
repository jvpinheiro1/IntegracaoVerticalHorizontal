from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)

inspecoes = []

@app.route('/inspecao', methods=['POST'])
def registrar_inspecao():
    dados = request.get_json()
    inspecao = {
        'id': str(uuid.uuid4()),
        'ordem_id': dados['ordem_id'],
        'descricao': dados['descricao'],
        'conforme': dados['conforme']
    }
    inspecoes.append(inspecao)

    # Integração com Certificadora se não conforme
    if not inspecao['conforme']:
        resposta = requests.post('http://certificadora:5000/verificar', json={
            'descricao': inspecao['descricao']
        })
        inspecao['certificadora'] = resposta.json()

    return jsonify(inspecao), 201

@app.route('/inspecao', methods=['GET'])
def listar_inspecoes():
    return jsonify(inspecoes)

@app.route('/nao-conformidades', methods=['GET'])
def listar_falhas():
    falhas = [i for i in inspecoes if not i['conforme']]
    return jsonify(falhas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

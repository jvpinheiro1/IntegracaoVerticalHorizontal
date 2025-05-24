from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ordens = []
contador_id = 1

@app.route('/ordens', methods=['POST'])
def criar_ordem():
    global contador_id
    dados = request.json
    ordem = {
        'id': contador_id,
        'modelo': dados.get('modelo'),
        'status': 'em produção',
        'etapas': []
    }
    ordens.append(ordem)
    contador_id += 1
    return jsonify(ordem), 201

@app.route('/ordens', methods=['GET'])
def listar_ordens():
    return jsonify(ordens)

@app.route('/ordens/<int:ordem_id>', methods=['GET'])
def buscar_ordem(ordem_id):
    for ordem in ordens:
        if ordem['id'] == ordem_id:
            return jsonify(ordem)
    return jsonify({'erro': 'Ordem não encontrada'}), 404

@app.route('/ordens/<int:ordem_id>/etapas', methods=['POST'])
def adicionar_etapa(ordem_id):
    dados = request.json
    for ordem in ordens:
        if ordem['id'] == ordem_id:
            etapa = {
                'descricao': dados.get('descricao'),
                'status': dados.get('status')
            }
            ordem['etapas'].append(etapa)
            return jsonify({'mensagem': 'Etapa adicionada com sucesso', 'ordem': ordem}), 200
    return jsonify({'erro': 'Ordem não encontrada'}), 404

@app.route('/ordens/<int:ordem_id>/etapas', methods=['GET'])
def listar_etapas(ordem_id):
    for ordem in ordens:
        if ordem['id'] == ordem_id:
            return jsonify(ordem['etapas'])
    return jsonify({'erro': 'Ordem não encontrada'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

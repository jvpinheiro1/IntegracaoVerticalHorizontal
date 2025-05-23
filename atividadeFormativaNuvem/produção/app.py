from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Banco de dados em memória (dicionário)
ordens_producao = {}

# Endpoint para criar nova ordem de produção
@app.route('/ordens', methods=['POST'])
def criar_ordem():
    dados = request.get_json()
    ordem_id = str(uuid.uuid4())
    nova_ordem = {
        'id': ordem_id,
        'modelo': dados.get('modelo'),
        'status': 'em andamento',
        'inicio': datetime.utcnow().isoformat()
    }
    ordens_producao[ordem_id] = nova_ordem
    return jsonify(nova_ordem), 201

# Endpoint para listar todas as ordens
@app.route('/ordens', methods=['GET'])
def listar_ordens():
    return jsonify(list(ordens_producao.values()))

# Endpoint para obter detalhes de uma ordem específica
@app.route('/ordens/<ordem_id>', methods=['GET'])
def obter_ordem(ordem_id):
    ordem = ordens_producao.get(ordem_id)
    if not ordem:
        return jsonify({'erro': 'Ordem não encontrada'}), 404
    return jsonify(ordem)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Para exemplo, vamos fazer requests para os outros serviços em localhost

@app.route('/dashboard')
def dashboard():
    try:
        ordens = requests.get('http://localhost:5001/ordens').json()
        inspecoes = requests.get('http://localhost:5002/inspecao').json()
        pecas = requests.get('http://localhost:5003/entrada').json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Falha na conexão com serviços internos', 'details': str(e)}), 500

    total_ordens = len(ordens)
    ordens_em_producao = sum(1 for o in ordens if o['status'] == 'Em produção')
    total_inspecoes = len(inspecoes)
    total_pecas = len(pecas)

    relatorio = {
        'total_ordens': total_ordens,
        'ordens_em_producao': ordens_em_producao,
        'total_inspecoes': total_inspecoes,
        'total_pecas': total_pecas,
    }
    return jsonify(relatorio)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

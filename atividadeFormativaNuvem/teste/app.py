from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASES = {
    'producao': 'http://producao:5001',
    'qualidade': 'http://qualidade:5002',
    'pecas': 'http://pecas:5002',
    'relatorios': 'http://relatorios:5004'
}

@app.route('/teste-integrado', methods=['GET'])
def testar():
    resultados = {}
    for nome, url in BASES.items():
        try:
            r = requests.get(url)
            resultados[nome] = f"OK ({r.status_code})"
        except Exception as e:
            resultados[nome] = f"Erro: {str(e)}"
    return jsonify(resultados)

@app.route('/dashboard-completo', methods=['GET'])
def dashboard():
    try:
        r = requests.get(f"{BASES['relatorios']}/dashboard")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

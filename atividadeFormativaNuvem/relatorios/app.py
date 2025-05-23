from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    producao = requests.get('http://producao:5000/ordens').json()
    qualidade = requests.get('http://qualidade:5000/inspecao').json()
    pecas = requests.get('http://pecas:5000/entrada').json()

    return jsonify({
        'total_ordens': len(producao),
        'inspecoes_realizadas': len(qualidade),
        'pecas_utilizadas': len(pecas),
        'falhas_detectadas': len([i for i in qualidade if not i['conforme']])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

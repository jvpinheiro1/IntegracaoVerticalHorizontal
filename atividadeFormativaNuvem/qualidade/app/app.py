from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

inspecoes = []

@app.route('/inspecao', methods=['GET', 'POST'])
def inspecao_handler():
    if request.method == 'POST':
        data = request.json
        inspecao = {
            'ordem_id': int(data.get('ordem_id')),
            'descricao': data.get('descricao'),
            'conforme': data.get('conforme', False)
        }
        inspecoes.append(inspecao)
        return jsonify(inspecao), 201
    else:
        return jsonify(inspecoes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

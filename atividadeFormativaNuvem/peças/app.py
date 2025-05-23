from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

pecas = []

@app.route('/entrada', methods=['GET', 'POST'])
def entrada_handler():
    if request.method == 'POST':
        data = request.json
        peca = {
            'codigo': data.get('codigo'),
            'descricao': data.get('descricao'),
            'vin': data.get('vin')
        }
        pecas.append(peca)
        return jsonify(peca), 201
    else:
        return jsonify(pecas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

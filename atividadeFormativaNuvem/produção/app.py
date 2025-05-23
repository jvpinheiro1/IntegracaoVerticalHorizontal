from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ordens = []
next_id = 1

@app.route('/ordens', methods=['GET', 'POST'])
def ordens_handler():
    global next_id
    if request.method == 'POST':
        data = request.json
        ordem = {
            'id': next_id,
            'modelo': data.get('modelo'),
            'status': 'Em produção'
        }
        next_id += 1
        ordens.append(ordem)
        return jsonify(ordem), 201
    else:
        return jsonify(ordens)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

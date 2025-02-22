from flask import Flask, jsonify
from flask_cors import CORS

app=Flask(__name__) 

CORS(app)

def custos(lucro,despesa,vendas):
    return {
        (lucro + despesa)/vendas
    }

print(custos(10000,3500,1000))


if __name__=='__main__':
    app.run(debug=True)
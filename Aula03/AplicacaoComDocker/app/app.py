from flask import Flask, request, jsonify, render_template
import mysql.connector

# Cria uma instância do Flask
app = Flask(__name__)

# Configuracões do banco de dados MySQL
db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'password', # Senha do MySQL
    'database': 'cadastro_db' # Nome do banco de dados

    # Nome do servico no docker-compose
    # Usuário do MySQL

}

# Rota principal: exibe o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastrar usuarios
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:  
        # Obtém os dados do formulário
        data = request.json
        nome = data['nome']
        email = data['email']
        # Conecta ao banco de dados
        conn = mysql.connector.connect( **db_config)
        cursor = conn. cursor()
        # Insere os dados no banco de dados
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email) )
        conn.commit() # Confirma a transacao
        # Fecha a conexao
        cursor.close()
        conn.close()
        #Retorna uma mensagem de sucesso
        return jsonify({"message": "Cadastro realizado com sucesso!"}), 200
    except Exception as e:
        # Retorna uma mensagem de erro
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
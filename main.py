from flask import Flask, request, make_response, jsonify
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#configurar o banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'usbw'
app.config['MYSQL_DB'] = 'helpme'

#inicializa o banco de dados e o marshmallow
mysql = MySQL(app)
ma = Marshmallow(app)

# Modelo de referencia da tabela users
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "nome", "email", "telefone", "senha")

user_schema = UserSchema()
user_schema = UserSchema(many = True)

# Rota para a listagem de usuarios
@app.route("/usuarios", methods =["GET"])
def get_users():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(result)) 

# Rota para cadastro de usuário
@app.route("/usuarios", methods =["POST"])
def add_use():
    nome = request.json["nome"]
    email = request.json["email"]
    telefone = request.json["telefone"]
    senha = request.json["senha"]
    
    cursor = mysql.connection.cursor()
    sql = f'''INSERT INTO users (nome, email, telefone, senha)
    values('{nome}','{email}', '{telefone}', '{senha}' )
    '''
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return make_response(jsonify({"message": "Success!"}))
   
# Rota para buscar usuario pelo id
@app.route("/usuarios/<id>", methods =["GET"])
def find_user_by_id(id):
    cursor = mysql.connection.cursor()
    sql = f"SELECT * from users WHERE id = {id}"
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return make_response(jsonify(result))

# Rota para editar os dados de um usuario
@app.route("/usuarios/update/<id>", methods =["PUT"])
def update_use(id):
    nome = request.json["nome"]
    email = request.json["email"]
    telefone = request.json["telefone"]
    senha = request.json["senha"]
    
    cursor = mysql.connection.cursor()
    sql = f'''
    UPDATE users SET 
    nome = '{nome}',
    email = '{email}',
    telefone = '{telefone}',
    senha = '{senha}'
    WHERE id = {id}
    '''
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return  make_response(jsonify({"message": "UPDATED!"}))

@app.route("/usuarios/delete/<id>", methods =["DELETE"])
def delete_user(id):
    cursor = mysql.connection.cursor()
    sql = f"DELETE from users WHERE id = {id}"
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return  make_response(jsonify({"message": "DONE!"}))

if __name__ == "__main__":
    app.run()
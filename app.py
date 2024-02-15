from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user , logout_user , login_required
from bcrypt import hashpw, checkpw, gensalt
from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# setando rota de login como login_view para o login manager
login_manager.login_view = 'login'

# rota de login @login_manager.user_loader carrega a
# sessão do usuário.
# Ela carrega o registro completo

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login',methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        #Busca se o usuário existe no banco (o primeiro)
        user = User.query.filter_by(username=username).first()

        if user and checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message":"Autenticação realizada com sucesso"}), 200

    return jsonify({"message":"Credenciais inválidas"}), 400


@app.route("/logout", methods=["GET"])
@login_required # protege rota apenas para usuários logados acessarem
def logout():
    logout_user() # desautentica o usuário
    return jsonify({"message":"Logout realizado com sucesso"}), 200

@app.route("/user",methods=["POST"])
@login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:
        #Busca se o usuário existe no banco (o primeiro)
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"message": "Usuario já cadastrado"}), 409
        hashed_password = hashpw(str.encode(password), gensalt())
        user = User(username=username,password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"}), 200
    return jsonify({"message":"Dados invalidos"}), 401

@app.route("/user/<int:id_user>",methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user:
        return jsonify({"username":user.username}), 200
    return jsonify({"message":"Usuário não encontrado"}), 404

@app.route("/user/<int:id_user>",methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)
    if id_user != current_user.id and current_user.role == 'user':
        return jsonify({"message": "Operação não permitida"}), 403

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message":f"Usuário {id_user} atualizado com sucesso"}), 200
    return jsonify({"message":"Usuário não encontrado"}), 404

@app.route("/user/<int:id_user>",methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida"}), 403
    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida ( o usuario logado está tentando deletar o próprio usuário)"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":f"Usuário {id_user} deletado com sucesso"}), 200
    
    return jsonify({"message":"Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)

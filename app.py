from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user , logout_user , login_required
from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

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

        if user and user.password == password:
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
        user = User(username=username,password=password)
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



@app.route("/hello-world")
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)

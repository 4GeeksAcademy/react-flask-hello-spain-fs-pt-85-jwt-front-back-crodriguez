"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from api.services import UserService
from flask_cors import cross_origin

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)

CORS(app)


app.url_map.strict_slashes = False
# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


@app.route('/api/sign_up', methods=['POST', 'OPTIONS'])
@cross_origin()
def signup():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    email = data["email"]
    password = data["password"]

    existing_user = UserService.exist(email)
    if existing_user:
        return jsonify({"error": "El usuario ya está registrado"}), 409

    new_user = UserService.create_user(email, password)
    access_token = create_access_token(identity=new_user.id)

    return jsonify({"message": "Usuario registrado con éxito", "token": access_token}), 201

@app.route('/log_in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Faltan datos"}), 400

        email = data["email"]
        password = data["password"]
        existing_user = userService.exist(email)

        if not existing_user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        access_token = create_access_token(identity=existing_user.id)

        return jsonify({"message": "Inicio de sesión exitoso", "token": access_token}), 200

    return jsonify({"message": "Bienvenido al endpoint de log_in. Realice un POST para iniciar sesión."}), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

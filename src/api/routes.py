"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)



# @api.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

@api.route('/user', methods=['GET'])
def handle_hello():
    try:
        data = db.session.scalars(select(User)).all()
        results = list(map(lambda item: item.serialize(), data))

        response_body = {
            "msg": "Hello, this is your GET /user response ",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error en /user: {e}")
        return jsonify({"error": "An error occurred"}), 500

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()

        if email == user.email or password == user.password:
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
            
    except:
         return jsonify({"msg": "Bad email or password"}), 401


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(logged_in_as=current_user), 200

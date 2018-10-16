import requests
import requests.exceptions
import json
from flask import Blueprint, jsonify, request as FlaskRequest
from flask_jwt_extended import ( jwt_required,
                                 create_access_token,
                                 get_jwt_identity )

authApi = Blueprint( 'auth', __name__ )



def registerApi( app, cors ):
    if app.config.get( "ALLOW_CORS_ORIGIN", False ):
        app.logger.info( "Allowing CORS" )
        origins = app.config.get( 'CORS_ORIGIN_WHITELIST', '*' )
        cors.init_app( authApi,
                       origins = origins )

    app.register_blueprint( authApi )
    return

@authApi.route( "/api/login", methods=[ 'POST' ] )
def login():
    if not FlaskRequest.is_json:
        return jsonify( { "msg": "Missing JSON in request" } ), 400

    username = FlaskRequest.json.get( 'username', None )
    password = FlaskRequest.json.get( 'password', None )
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != '12345678':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token( identity = username )
    return jsonify( access_token = access_token ), 200


@authApi.route('/api/protected', methods=['POST'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify( logged_in_as = current_user ), 200

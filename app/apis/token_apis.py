from app import app
from app.models import User
from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token
from webargs import fields
from webargs.flaskparser import parser


@app.route('/login', methods=['POST'])
def post_login():
    json = parser.parse({
        'username': fields.Str(required=True),
        'password': fields.Str(required=True),
    }, request)
    user = User.query.filter_by(**json).first()
    if not user:
        abort(401)

    access_token = create_access_token(identity=json['username'])
    return jsonify(access_token=access_token)

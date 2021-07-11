from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.util import ResponseException

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)

from app.apis import *
from app.view import *


@app.errorhandler(ResponseException)
def handle_exception(e):
    return e.response()


@app.errorhandler(422)
def handle_error_422(e):
    data = e.data.get('messages', ['invalid request'])
    return ResponseException(e.code, 'Unprocessable Entity', data).response()


@jwt.unauthorized_loader
@jwt.expired_token_loader
@jwt.invalid_token_loader
def handle_error_401(msg, expired=None):
    message = msg if not expired else 'Token has expired' 
    data = {
        'headers': {
            'Authorization': [ message ]
        }
    }
    return ResponseException(401, 'Unauthorized', data).response()

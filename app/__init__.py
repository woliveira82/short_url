from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.apis import *
from app.view import *

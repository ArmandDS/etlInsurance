from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,jwt_optional, get_jwt_identity, get_raw_jwt)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)



application.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

#application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testflask:Test2019--@mydbinsurance.cw3mhyuafkex.eu-west-1.rds.amazonaws.com:3306/mydbinsurance'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/insurance.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SECRET_KEY'] = 'some-secret-string'
application.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(application)

db = SQLAlchemy(application)










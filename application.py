"""
Main module of the server file
"""

# 3rd party moudles

from flask import render_template, Flask
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,jwt_optional, get_jwt_identity, get_raw_jwt)
from flask.json import jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pandas as pd
import numpy as np
from flask_restful import Api
from flask_jwt_extended import JWTManager
# Local modules

from  data import etl
from sqlalchemy.engine import create_engine, Engine
from api.report import *
import config





application = config.application
api = config.api
jwt = JWTManager(application)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)




import models
import  resources

api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.CashReport, '/cashreport', '/cashreport/agency/<int:agency_id2>')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.ProfitabilityAgency, '/profitability', '/profitability/agency/<int:agency_id2>','/profitability/agency/<int:agency_id2>/year/<int:year>')
api.add_resource(resources.AllData, '/alldata')
api.add_resource(resources.AllAgencies, '/allagencies')
api.add_resource(resources.AllProducts, '/allproducts')
api.add_resource(resources.AgenciesId, '/agenciesid')
api.add_resource(resources.AgenciesYear, '/agenciesyear',  '/agenciesyear/<int:agency_id>')
api.add_resource(resources.AllRevenues, '/revenues',  '/revenues/agency/<int:agency_id>', '/revenues/agency/<int:agency_id>/year/<int:year>')
api.add_resource(resources.Clustering, '/clustering')


@application.route('/')
@application.route('/signin')
def signin():
    return render_template("signin.html")


@application.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if request.cookies.get('name'):
        logger.debug(request.cookies.get('name'))
        return render_template("dashboard.html")
    else:
        return render_template("signin.html")





@application.before_first_request
def create_tables():
    db.create_all()
    etl.main()
    
    
    

if __name__ == '__main__':
    application.debug = True
    application.run()
    

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 18:49:45 2019

@author: Usuario
"""

from application import application
from flask import jsonify
from flask import render_template, Flask, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,jwt_optional, get_jwt_identity, get_raw_jwt)
from flask_restful import reqparse
import logging

#Create and configure logger 
logging.basicConfig(filename="report.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w+') 

logger=logging.getLogger()



@application.route('/')
@application.route('/signin')
def signin():
    return render_template("signin.html")


@application.route('/dashboard')
def dashboard():
    if request.cookies.get('name'):
        logger.debug(request.cookies.get('name'))
        return render_template("dashboard.html")
    else:
        return render_template("signin.html")


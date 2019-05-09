# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:30:31 2019

@author: Usuario
"""


import pandas as pd
import numpy as np
from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import time 
from sqlalchemy.engine import create_engine, Engine
from flask import make_response, abort, request, jsonify, Response
from data.etl import *
from api.report import *
import json
from collections import OrderedDict, defaultdict
import datetime
import logging

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = False)

#Create and configure logger 
logging.basicConfig(filename="resources.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger()



class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            if UserModel.find_by_username(data['username']):
                return {'message': 'User {} already exists'. format(data['username'])}
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200
        except Exception as e:
            logger.error(f"There was an error: {e}") 
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            expires = datetime.timedelta(hours=1)
            access_token = create_access_token(identity = data['username'], expires_delta=expires)
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': '{}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200
        else:
            logger.error(f"There was an error: 401") 
            return {'message': ''}, 401
        


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except Exception as e:
            logger.error(f"There was an error: {e}") 
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except Exception as e:
            logger.error(f"There was an error: {e}") 
            return {'message': 'Something went wrong'}, 500
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()
      
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42}
        


def query_with_all(data_frame, query_string):
    if query_string == "all":
        return data_frame
    return data_frame.query(query_string)

def export_file(df, fname, dest):
    if dest == "csv":
        filepath =  (f"{fname}")
        df.to_csv(filepath, chunksize=1000)
    elif dest =="print":
        print(df)
    else:
        pass


class CashReport(Resource):
    
    @jwt_required
    def get(self, agency_id2 ="" ) :
        agency_id =  agency_id2
        engine = connect()
        agency_param=""
        dest=""        
        data = cash_report(engine, agency_id,  agency_param, dest).reset_index()
        lista_dicc = []
        cnames = data.reset_index().columns[1:]
        dicc_names ={}
        for i,c in enumerate(cnames):
            key = "column"+str(i)
            dicc_names[key] = c
            
        lista_dicc.append(dicc_names)
        for c,r in data.iterrows():
            dicc= {}
            dicc["AGENCY_ID"] = r['AGENCY_ID']
            dicc["PROD_ABBR"] = r['PROD_ABBR']
            for i in range(len(cnames[2:])): 
                dicc["YEAR"+str(i+1)] = r[data.columns[i+2]]
                dicc["YEAR5"] = r[data.columns[6]]
            lista_dicc.append(dicc)
        return json.dumps(lista_dicc)
        
        
        
class ProfitabilityAgency(Resource):
    @jwt_required    
    def get(self, agency_id2="", year="") :
        agency_id =  agency_id2
        engine = connect()
        data = profitability_agency( engine, agency_id, year, dest="")
        lista_dicc =[]
        cnames = data.reset_index().columns
        lista_dicc.append({"column1": cnames[0], "columns2":cnames[1]})
        for x,i in data.iterrows():
            dicc ={}
            dicc["name"] = x
            dicc["value"] = i[data.columns[0]]
            lista_dicc.append(dicc)
        return json.dumps(lista_dicc), 200
            
    
        
        
        
class AllData(Resource):
    @jwt_required     
    def get(self):
        engine = connect()
        data = all_data(engine)
        # lista_dicc =[]
        # dicc= {}
        # data= data.reset_index()
        # cnames = data.columns
        # dicc_names ={}
        # for i,c in enumerate(cnames):
        #     key = "column"+str(i)
        #     dicc_names[key] = c
        # lista_dicc.append(dicc_names)
        # dd = defaultdict(list)
        # lista_dicc.append(data.to_dict('records', into=dd))
        return Response(
        data.to_csv(chunksize=1000),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=data.csv"})

        
        
        
        
        
class AllAgencies(Resource):
    @jwt_required         
    def get(self):
        logger.info(f"Creating List of all Agencies...")
        engine = connect()
        data = agencies_all(engine)
        lista_dicc =[]
        cnames = data.columns
        dicc_names ={}
        for i,c in enumerate(cnames):
            key = "column"+str(i)
            if i !=0:
                dicc_names[key] = c
        lista_dicc.append(dicc_names)
        dd = defaultdict(list)
        lista_dicc.append(data.to_dict('records', into=dd))
        return json.dumps(lista_dicc), 200
 
        
class AllProducts(Resource):
    @jwt_required   
    def get(self):
        engine = connect()
        data = products_all(engine)
        lista_dicc =[]
        cnames = data.columns
        dicc_names ={}
        for i,c in enumerate(cnames):
            key = "column"+str(i)
            if i !=0:
                dicc_names[key] = c
        lista_dicc.append(dicc_names)
        for c,r in data.iterrows():
            dicc= {}
            dicc["PROD_ABBR"] = r['PROD_ABBR']
            dicc["PROD_LINE"] = r['PROD_LINE']
            lista_dicc.append(dicc)
        return json.dumps(lista_dicc),200
 

class AllRevenues(Resource):
    @jwt_required         
    def get(self, agency_id="", year =""):
        logger.info(f"Creating List of all Revenues...")
        engine = connect()
        data = revenues(engine, agency_id, year)
        lista_dicc =[]
        cnames = data.columns
        dicc_names ={}
        for i,c in enumerate(cnames):
            key = "column"+str(i)
            if i !=0:
                dicc_names[key] = c
        lista_dicc.append(dicc_names)
        dd = defaultdict(list)
        lista_dicc.append(data.to_dict('records', into=dd))
        return json.dumps(lista_dicc), 200

class Clustering(Resource):
    @jwt_required         
    def get(self):
        logger.info(f"Creating List of Clustering...")
        engine = connect()
        data = getClusters(engine)
        lista_dicc =[]
        cnames = data.columns
        dicc_names ={}
        for i,c in enumerate(cnames):
            key = "column"+str(i)
            if i !=0:
                dicc_names[key] = c
        lista_dicc.append(dicc_names)
        dd = defaultdict(list)
        lista_dicc.append(data.to_dict('records', into=dd))
        return json.dumps(lista_dicc), 200
 



class AgenciesId(Resource):
    @jwt_required
    def get(self):
        return json.dumps(agencies_id(connect()).values.tolist())


class AgenciesYear(Resource):
    @jwt_required   
    def get(self, agency_id=""):
        print("DUMP",json.dumps(agencies_year(connect(), agency_id).values.tolist()))
        return json.dumps(agencies_year(connect(), agency_id).values.tolist())

    

        

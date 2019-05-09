# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 11:52:29 2019

@author: Usuario
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
from click import Context
import logging
from os.path import join, dirname, abspath
from sqlalchemy import INTEGER, DECIMAL, VARCHAR, CHAR
from sqlalchemy.engine import create_engine, Engine
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
sys.path.insert(0, '..')
from  config import *



#Create and configure logger 
logging.basicConfig(filename="etl.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 

def connect():
    '''
    Input:
       None
    Output:
        DB Connection
    '''    
    logger.info("Connecting to insurance.db...")
    try:
        if __name__ == '__main__':
           db_path = 'sqlite:///insurance.db'
        else:
            db_path = application.config['SQLALCHEMY_DATABASE_URI']
        return create_engine(db_path)
    except Exception as e:
        logger.error(f"Unable to connect to the database: {e}")
        return {"message": f"error {e}"}

def clean_data(df =  pd.DataFrame ):
    '''
    Input:
       df: raw dataset
    Output:
        df: cleaned dataset
    '''  
    df = df.copy()
    df = df.round(2)
    df = df[df['PRIMARY_AGENCY_ID']!=99999]
    
    for  col in df.describe().columns.tolist():
        if col.find("YEAR") == -1:
            df_col_mode = df[col].mode()[0]
            if df_col_mode !=99999:
                df[col].replace(99999,df_col_mode,  inplace=True)
            else:
                df_col_mode = df[col][df[col]!=99999].median()
                df[col].replace(99999,df_col_mode,  inplace=True)
    return df


def load_data(engine: Engine):
    '''
    Input:
       engine: a db connection
    Output:
        df: saved dataset
    '''  
    logger.info("Loading the staging table...")
    #csv_path = os.path.join(ROOT_DIR, "finalapi.csv")
    basedir = os.getcwd()
    if __name__ == '__main__':
        csv_path = os.path.join(basedir,  "finalapi.csv")
    else:
        csv_path = os.path.join(basedir, "data", "finalapi.csv")
    
    try:
        df = pd.read_csv(csv_path)
        df_c = clean_data(df)
        logger.info("Cleaning the Data...")
        df_c.to_sql("staging", con=engine, if_exists="replace", index=False, chunksize = 30)
        logger.info("End Load")
    except Exception as e: 
        logger.error(f"There was an error loading finalapi.csv to the staging table: {e}")
        raise
    else:
        logger.info("The staging table was successfully loaded.")
        return df



def load_product_dim(engine: Engine, data: pd.DataFrame):
    '''
    Input:
       engine: a db connection
       data : dataset to filter
    Output:
        df: saved dataset
    ''' 
    logger.info("Loading the product_dim table...")
    try:
        df = data[["PROD_ABBR", "PROD_LINE"]].drop_duplicates()
        df.to_sql("product_dim", con=engine, if_exists="replace")
    except Exception as e:
        logger.error(f"There was an error loading the product_dim table: {e}")
        raise
    else:
        logger.info("The product_dim table was successfully loaded.")
        #return df



def load_revenue_fact(engine: Engine, staging: pd.DataFrame):
    '''
    Input:
       engine: a db connection
       data : dataset to filter
    Output:
        df: saved dataset of revenue fact
    ''' 
    logger.info("Loading the revenue_fact...")
    try:
        df = staging.pivot_table(
            index=[
                "AGENCY_ID",
                "PROD_ABBR",
                "STATE_ABBR",
                "STAT_PROFILE_DATE_YEAR"
            ],
            values=[
                "PRD_ERND_PREM_AMT",
                "POLY_INFORCE_QTY",
                "WRTN_PREM_AMT"
            ],
            aggfunc=np.sum
        )
                
        df.to_sql(
            name="revenue_fact",
            con=engine,
            if_exists="replace",
            dtype={
                "AGENCY_ID": INTEGER(),
                "PROD_ABBR": VARCHAR(40),
                "STATE_ABBR": CHAR(2),
                "STAT_PROFILE_DATE_YEAR": INTEGER(),
                "PRD_ERND_PREM_AMT": DECIMAL(19, 2),
                "POLY_INFORCE_QTY": DECIMAL(19, 2),
                "WRTN_PREM_AMT": DECIMAL(19, 2)
            }, chunksize = 30
        )
    except Exception as e:
        logger.error(f"There was an error loading the revenue_fact: {e}")
        raise
    else:
        logger.info("The revenue_fact was successfully loaded.")
        #return df




def load_agency_dim(engine: Engine, data: pd.DataFrame):
    '''
    Input:
       engine: a db connection
       data : dataset to filter
    Output:
        df: saved dataset of agency dim
    ''' 
    logger.info("Loading agency_dim...")
    try:
        df = data[[
            "AGENCY_ID",
            "PRIMARY_AGENCY_ID",
            "VENDOR",
            "ACTIVE_PRODUCERS",
            "AGENCY_APPOINTMENT_YEAR",
            "VENDOR_IND"
        ]].drop_duplicates()
        df.to_sql("agency_dim", con=engine, if_exists="replace", chunksize= 30)
    except Exception as e:
        logger.error(f"There was an error loading the agency_dim table: {e}")
    else:
        logger.info("The agency_dim was successfully loaded.")
        #return df

def load_cluster_dim(engine: Engine, data: pd.DataFrame):
    '''
    Input:
       engine: a db connection
       data : dataset to filter
    Output:
        df: saved dataset of cluster info
    ''' 
    logger.info("Loading cluster_dim...")
    try:
        df = pd.read_sql(sql="SELECT  AGENCY_ID, STAT_PROFILE_DATE_YEAR, RETENTION_POLY_QTY,\
                         POLY_INFORCE_QTY, PREV_POLY_INFORCE_QTY,\
                         NB_WRTN_PREM_AMT, WRTN_PREM_AMT, PREV_WRTN_PREM_AMT,\
                         PRD_ERND_PREM_AMT, PRD_INCRD_LOSSES_AMT, \
                         RETENTION_RATIO, LOSS_RATIO, LOSS_RATIO_3YR, GROWTH_RATE_3YR from staging", con=engine)
        df_numerical = df.groupby(['AGENCY_ID']).mean()
       
        kmeans = KMeans(n_clusters=4)
        scaler = MinMaxScaler()
        df_numerical_std = scaler.fit_transform(df_numerical)
        reduced_data = PCA(n_components=2).fit_transform(df_numerical_std)
        kmeans.fit(df_numerical_std)
        labels = kmeans.labels_ + 1
        df_cluster = pd.DataFrame(columns = ['x_axis', 'y_axis', 'labels', 'AGENCY_ID'])
        df_cluster['x_axis'] = reduced_data[:, 0]
        df_cluster['y_axis'] =reduced_data[:, 1]
        df_cluster['labels']= labels
        df_cluster['AGENCY_ID'] = df_numerical.reset_index(['AGENCY_ID'])
        df_cluster.to_sql("cluster_dim", con=engine, if_exists="replace", chunksize= 30)
    except Exception as e:
        logger.error(f"There was an error loading the cluster_dim table: {e}")
    else:
        logger.info("The cluster_dim was successfully loaded.")
        return df_cluster






def main():
    logger.info("Loading the data warehouse...")
    c = connect()
    df = load_data(c)
    load_revenue_fact(c , df)
    load_agency_dim(c,df)
    load_product_dim(c, df)
    load_cluster_dim(c, df)
    logger.info("The data warehouse was loaded successfully.")



if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 17:23:59 2019

@author: Usuario
"""

import numpy as np
import pandas as pd
import time
import sys
import argparse

from sqlalchemy.engine import create_engine, Engine
from flask import make_response, abort
try:
    from data.etl import *
except:
    sys.path.insert(0, '../data')
    from etl import *

#Create and configure logger 
logging.basicConfig(filename="etl.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger()



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



def cash_report(engine: Engine, agency_id: int,  agency_param="", dest="") :
    logger.info(f"Creating report for the last 5 years of net cash flows for an agency {agency_id} {agency_param}...")
    
    try:

        if agency_id=="" and agency_param =="":
            query_string = "all"
        elif agency_id !="":
            query_string = f"AGENCY_ID == {agency_id}"
        else:
            query_string = f"AGENCY_ID == {agency_param}"
        cash_flows = pd.read_sql(sql="staging", con=engine)
        cash_flows =(query_with_all(cash_flows, query_string).assign(net_cash_flows=lambda df: df.PRD_ERND_PREM_AMT - df.PRD_INCRD_LOSSES_AMT)
            .pivot_table(
                index=["AGENCY_ID", "PROD_ABBR"],
                columns=["STAT_PROFILE_DATE_YEAR"],
                values="net_cash_flows",
                aggfunc=np.sum
            )
            .fillna(0)
            .round(2)
            .iloc[:, -5:]
        )
        export_file(cash_flows,"cash_flow.csv", dest )

    except Exception as e:
        logger.error(f"There was an error exporting the net cash flows dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return cash_flows
    
    
    

def revenues(engine: Engine, agency_id: int, year: int, dest="") -> pd.DataFrame:
    logger.info(f"Creating revenues report for agency {agency_id} for {year}...")
    
    try:
        if agency_id=="":
            query_string = "all"
        elif year =="":
            query_string = f"AGENCY_ID == {agency_id}"
        elif not str(year).isnumeric():
            query_string = f"AGENCY_ID == {agency_id}"
        else:
            query_string = f"AGENCY_ID == {agency_id} & STAT_PROFILE_DATE_YEAR == {year}"

        revenues = ( pd.read_sql(sql="revenue_fact", con=engine)).reset_index() 
        revenues = (query_with_all(revenues,query_string))
        export_file(revenues,"revenues_facts.csv", dest )
    except Exception as e:
        logger.error(f"There was an error exporting the revenue dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return revenues
    


def profitability_agency(engine: Engine, agency_id: int, year: int, dest="") -> pd.DataFrame:
    logger.info(f"Creating profitability report for agency {agency_id} for {year}...")
    try:
        if agency_id=="":
            query_string = "all"
        elif year =="":
            query_string = f"AGENCY_ID == {agency_id}"
        elif not str(year).isnumeric():
            query_string = f"AGENCY_ID == {agency_id}"
        else:
            query_string = f"AGENCY_ID == {agency_id} & STAT_PROFILE_DATE_YEAR == {year}"
        profitability = ( pd.read_sql(sql="staging", con=engine)) 
        profitability = (query_with_all(profitability,query_string).pivot_table(values="WRTN_PREM_AMT", index="PROD_ABBR", aggfunc=np.sum)
            .sort_values(by="WRTN_PREM_AMT", ascending=False))
        export_file(profitability,"profitability.csv", dest )
    except Exception as e:
        logger.error(f"There was an error exporting the profitability dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return profitability
    
    


    
    
    

def all_data(engine: Engine, dest=""):
    logger.info(f"Creating The File of all data ...")
    try:
        summary = (
            pd.read_sql(sql="staging", con=engine).set_index(['AGENCY_ID','STAT_PROFILE_DATE_YEAR']) )
        export_file(summary,"all_data.csv", dest )
    except Exception as e:
        logger.error(f"There was an error exporting the dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return summary  
    
    
    
    
    
def agencies_all(engine: Engine, dest=""):
    logger.info(f"Creating List of all Agencies...")
    try:
        agencies = (
            pd.read_sql(sql="agency_dim", con=engine)
        )
        export_file(agencies,"agencies_dim.csv", dest )
    except Exception as e:
        logger.error(f"There was an error exporting the dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return agencies

def products_all(engine: Engine, dest=""):
    logger.info(f"Creating List of all Products...")
    try:
        products = (
            pd.read_sql(sql="product_dim", con=engine)
        )
        export_file(products,"products_dim.csv", dest )
    except Exception as e:
        logger.error(f"There was an error exporting the dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        logger.debug("RETURNING")
        return products
    
    
    
def agencies_id(engine: Engine):
    logger.info(f"Returning unique id...")
    try:
        agencies_id = (
            pd.read_sql(sql=f"SELECT DISTINCT AGENCY_ID FROM staging WHERE   STAT_PROFILE_DATE_YEAR IS NOT NULL;", con=engine) )
        
    except Exception as e:
        logger.error(f"There was an error getting lla agencies id: {e}")
        return{'message': f'Something went wrong {e}'}, 500
    else:
        return agencies_id 
    
def agencies_year(engine: Engine, agency="all"):
    logger.info(f"Returning unique Year...")
    try:
        agenciesYear = (
            pd.read_sql(sql=f"SELECT DISTINCT STAT_PROFILE_DATE_YEAR FROM staging WHERE AGENCY_ID={agency};", con=engine) )
        
    except Exception as e:
        logger.error(f"There was an error exporting the dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return agenciesYear 

def getClusters(engine: Engine, dest=""):
    logger.info(f"Returning Cluters...")
    try:
        df_cluster = (
            pd.read_sql(sql=f"cluster_dim", con=engine) )
        export_file(df_cluster,"clusters.csv", dest )
    except Exception as e:
        logger.error(f"There was an error exporting the dataset: {e}")
        return{'message': 'Something went wrong'}, 500
    else:
        return df_cluster



 
def main():
    db_path = 'sqlite:///../data/insurance.db'
    c = create_engine(db_path)
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', '--d', help="Save the csv or print the return function", type= str)
    args, param = parser.parse_known_args()
    if sys.argv[1] == "cash_report":
        try:
            agency_param =  param[1]
        except:
            agency_param =  ""
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        print(agency_param)
        cash_report(c, "", agency_param, save_param)
    elif sys.argv[1] =="profitability":
        try:
            agency_param =  param[1]
        except:
            agency_param =  ""
        try:
            year_param =  param[2]
        except:
            year_param =  ""
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        profitability_agency(c,  agency_param, year_param, save_param)
    elif sys.argv[1] =="revenues":
        try:
            agency_param =  param[1]
        except:
            agency_param =  ""
        try:
            year_param =  param[2]
        except:
            year_param =  ""
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        revenues(c,  agency_param, year_param, save_param)
    elif sys.argv[1] =="all_data":
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        all_data(c,  save_param)
    elif sys.argv[1] =="agencies_dim":
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        agencies_all(c,  save_param)
    elif sys.argv[1] =="products_dim":
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        products_all(c,  save_param)
    elif sys.argv[1] =="cluster":
        try:
            save_param =  args.dest
        except:
            save_param =  ""
        getClusters(c,  save_param)


if __name__ == "__main__":
    main()

import os
import sys
from src.Demo_Project.exception import CustomException
from src.Demo_Project.logger import logging
import pandas as pd
from dotenv import load_dotenv
import psycopg2

import pickle



load_dotenv()
host=os.getenv("host")
username=os.getenv("username")
port=os.getenv("port")
db=os.getenv("db")
password=os.getenv("password")
def read_sql_data():
    logging.info("reading sql database started")
    try:
        mydb=psycopg2.connect(
            host=host,
            port=port,
            database=db,
            user=username,
            password=password
        )
        logging.info("connection established",mydb)
        df=pd.read_sql_query("select * from payment",mydb)
        print(df.head)
        return df
    except Exception as ex:
        raise CustomException(str(ex),sys)

def save_obj(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
    
        with open (file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(str(e),sys)
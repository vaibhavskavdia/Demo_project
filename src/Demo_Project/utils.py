import os
import sys
from src.Demo_Project.exception import CustomException
from src.Demo_Project.logger import logging
import pandas as pd
from dotenv import load_dotenv
import psycopg2

load_dotenv()
host=os.getenv("host")
username=os.getenv("username")
port=os.getenv("port")
db=os.getenv("db")

def read_sql_data():
    logging.info("reading sql database started")
    try:
        mydb=psycopg2.connect(
            host=host,
            port=port,
            database=db,
            user=username
            password="12345"
        )
        logging.info("connection established",mydb)
        df=pd.read_sql_query("select * from customer",mydb)
        print(df.head)
        return df
    except Exception as ex:
        raise CustomException(str(ex),sys)
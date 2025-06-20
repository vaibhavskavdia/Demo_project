import os
import sys
from src.Demo_Project.exception import CustomException
from src.Demo_Project.logger import logging
import pandas as pd
from dotenv import load_dotenv
import psycopg2

import pickle

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
    
        with open (file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(str(e),sys)
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise CustomException(str(e),sys)
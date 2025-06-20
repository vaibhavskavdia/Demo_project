import sys 
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import os
from src.Demo_Project.utils import save_object
from src.Demo_Project.exception import CustomException
from src.Demo_Project.logger import logging

@dataclass
class DataTransformationConfig:
    #creating a pickle file in artifacts folder that saves the feature engineered data
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        
    def get_data_transformer_object(self):
        #this function is responsible for data transformation
        try:
            numerical_columns=["payment_id","staff_id"]
            categorical_columns=[]
            num_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='median')),
                ("scalar",StandardScaler())
            ])
            cat_pipepline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='most_frequent')),
                ("encoder",OneHotEncoder()),
                ("scalar",StandardScaler(with_mean=False))
            ])
            logging.info("categorical columns:{categorical_columns}")
            logging.info("numerical columns:{numerical_columns}")
            
            preprocessor=ColumnTransformer(
                ("num_pipeline",num_pipeline,numerical_columns),
                ("categorical_pipeline",cat_pipepline,categorical_columns)
            )
            return preprocessor
            
        except Exception as e:
            raise CustomException(str(e),sys)
    #train path and test path are the output of data ingestion ,now that goes into our data transformation
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("reading test train files")
            preprocessor_obj=self.get_data_transformer_object()
            target_column="amount"
            numerical_columns=["payment_id","staff_id"]
            #dividing dependent and indepenedent features of train dataset
            input_features_train_df=train_df.drop(columns=[target_column],axis=1)
            target_features_train_df=train_df[target_column]
            #dividing dependent and indepenedent features of test dataset
            input_features_test_df=test_df.drop(columns=[target_column],axis=1)
            target_features_test_df=test_df[target_column]
            
            logging.info("preprocessing")
            input_features_training_arr=preprocessor_obj.fit_transform(input_features_train_df)
            input_features_test_arr=preprocessor_obj.transform(input_features_test_df)
            
            #finally concatenating back the complete data
            train_arr=np.c_[input_features_training_arr,np.array(target_features_train_df)]
            test_arr=np.c_[input_features_test_arr,np.array(target_features_test_df)]
            
            logging.info("joined back the feature engineered data")
            #now to save this in a pickle file so that it can be extracted and used in other places 
            #we will make a function in utils.py that will make a common functionality to operate this

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj)
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(str(e),sys)
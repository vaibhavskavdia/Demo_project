from src.Demo_Project.logger import logging
from src.Demo_Project.exception import CustomException
import sys
from src.Demo_Project.components.data_ingestion import DataIngestionConfig
from src.Demo_Project.components.data_ingestion import DataIngestion
from src.Demo_Project.components.data_transformation import DataTransformationConfig,DataTransformation

if __name__=="__main__":
    logging.info("execution has started")
    
    try:
        #data_ingestion_config=DataIngestionConfig()
        data_ingestion=DataIngestion()
        data_ingestion.initiate_data_config()
        
        data_transformation=DataTransformation()
        train_data_path,test_data_path=data_transformation.initiate_data_transformation()
        
    except Exception as e:
        logging.info("custom exception")
        raise CustomException(e,sys)
from src.Demo_Project.logger import logging
from src.Demo_Project.exception import CustomException
import sys
from src.Demo_Project.components.data_ingestion import DataIngestionConfig
from src.Demo_Project.components.data_ingestion import DataIngestion


if __name__=="__main__":
    logging.info("execution has started")
    
    try:
        #data_ingestion_config=DataIngestionConfig()
        data_ingestion=DataIngestion()
        data_ingestion.initiate_data_config()
        
    except Exception as e:
        logging.info("custom exception")
        raise CustomException(e,sys)
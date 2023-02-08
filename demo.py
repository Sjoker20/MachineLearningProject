from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingExceptions
from housing.logger import logging
import os,sys
from housing.config.configuration import Configuartion
from housing.component.data_transformation import DataTransformation
from housing.util.util import *

def main():
    try:
        pipeline= Pipeline()
        pipeline.run_pipeline()
        # data_transformation_config = Configuartion().get_data_transformation_config()
        # print(data_transformation_config)
        # schema_file_path=r"C:\Users\kushanu\Documents\GitHub_Projects_Ineuron\MachineLearningProject\config\schema.yaml"
        # file_path=r"C:\Users\kushanu\Documents\GitHub_Projects_Ineuron\MachineLearningProject\housing\artifact\data_ingestion\2023-01-30-16-51-04\ingested_data\train\housing.csv"

        # df=load_data(file_path=file_path,schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)
        
    except Exception as e:
        logging.error(f"{e}")
        raise HousingExceptions(e,sys) from e

if __name__=='__main__':
    main()



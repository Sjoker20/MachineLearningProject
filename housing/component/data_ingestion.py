from housing.entity.config_entity import DataIngestionConfig
from housing.exception import HousingExceptions
import sys,os
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:
    
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data Ingestion log started {'='*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingExceptions (e,sys) from e



    def download_housing_data(self)-> str:
        try:
            #extraction remote url to dataset url
            download_url = self.data_ingestion_config.dataset_download_url
            # Folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            #create the tgz folder if already not available
            os.makedirs(tgz_download_dir, exist_ok=True)
            
            housing_file_name=  os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir,housing_file_name)
            logging.info(f" Downloading file from: [{download_url}] to file location: [{tgz_file_path}]")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f" File [{tgz_file_path}] is successfully downloaded.")
            return tgz_file_path

        except Exception as e:
            raise HousingExceptions(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir, exist_ok=True)

            # housing_tgz_file_obj = tarfile.open(tgz_file_path)
            # housing_tgz_file_obj.extractall(path=raw_data_dir)
            # housing_tgz_file_obj.close()
            logging.info(f"Extracting file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Extracting completed into dir: [{raw_data_dir}]")

        except Exception as e:
            raise HousingExceptions(e, sys) from e
        

    def split_file_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]

            housing_file_path =os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv files: [{housing_file_path}]")
            housing_data_frame = pd.read_csv(housing_file_path)

            housing_data_frame["income_cat"]= pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0 ,1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set= None

            split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2, random_state = 42)

            for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"], axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"], axis=1)
            
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)
            
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                        test_file_path=test_file_path,
                                        is_ingested=True,
                                        message=f"Data ingestion is completed successfully.")
            logging.info(f"Data ingestion Artifact: [{data_ingestion_artifact}]")

            return data_ingestion_artifact

        except Exception as e:
            raise HousingExceptions(e, sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_file_as_train_test()

        except Exception as e:
            raise HousingExceptions(e,sys) from e


    def __del__(self):
        logging.info(f"{'='*20}Data ingestion log completed {'='*20} /n/n")

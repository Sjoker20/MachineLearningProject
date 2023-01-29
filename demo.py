from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingExceptions
from housing.logger import logging
import os,sys


def main():
    try:
        pipeline= Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        raise HousingExceptions(e,sys) from e

if __name__=='__main__':
    main()
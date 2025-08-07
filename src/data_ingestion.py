# src/data_ingestion.py
import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
import sys

from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import RAW_DIR, RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_PATH
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config: dict):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion initialized for bucket: '{self.bucket_name}', file: '{self.file_name}'")

    def download_csv_from_gcp(self):
        try:
            logger.info(f"Attempting to download '{self.file_name}' from GCP bucket '{self.bucket_name}'...")
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File downloaded from GCP bucket '{self.bucket_name}' to '{RAW_FILE_PATH}' successfully.")
        except Exception as e:
            logger.error(f"Error downloading file from GCP bucket: {e}", exc_info=True)
            raise CustomException("Failed to download file from GCP bucket", sys.exc_info()) from e

    def split_data(self):
        try:
            logger.info("Loading raw data for splitting...")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1 - self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Data split into train and test sets. Train data saved to {TRAIN_FILE_PATH}, Test data saved to {TEST_FILE_PATH}.")
        except Exception as e:
            logger.error(f"Error during data splitting: {e}", exc_info=True)
            raise CustomException("Failed to split data", sys.exc_info()) from e

    def run(self):
        try:
            logger.info("Starting data ingestion process...")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion completed successfully.")
        except Exception as e:
            logger.error(f"Data ingestion process failed: {e}", exc_info=True)
            raise CustomException("Data ingestion failed", sys.exc_info()) from e

if __name__ == "__main__":
    try:
        config = read_yaml(CONFIG_PATH)
        data_ingestion = DataIngestion(config)
        data_ingestion.run()
    except Exception as e:
        logger.error(f"An unexpected error occurred in the main execution block: {e}", exc_info=True)
        raise CustomException("An unexpected error occurred during data ingestion execution", sys.exc_info()) from e
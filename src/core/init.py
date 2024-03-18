import os
import logging

from src.settings.config import settings
from src.settings.log import DEFAULT_LOGGING


async def init_log_folder():
    directory_path = settings.LOGS_FOLDER
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            logging.info(f"Directory '{directory_path}' created successfully.")
        except Exception as e:
            logging.error(f"Error creating directory '{directory_path}': {e}")


async def configure_logging():
    log_settings = DEFAULT_LOGGING
    logging.config.dictConfig(log_settings)
    logging.info("Logging settings is activate")


async def ensure_media_directory_exists():
    directory_path = settings.MEDIA_FOLDER
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            logging.info(f"Directory '{directory_path}' created successfully.")
        except Exception as e:
            logging.error(f"Error creating directory '{directory_path}': {e}")
    else:
        logging.info(f"Directory '{directory_path}' already exists.")

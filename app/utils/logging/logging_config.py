# Imports libraries
import logging

# Local imports
from app.settings import settings


# Logger Setup
LEVEL = settings.LOG_LEVEL


def setup_logging():
    # Set up the basic logging configuration
    logging.basicConfig(
        level=LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                "app/logs/debug.log"),  # Log to a file
            logging.StreamHandler()  # Log to the console
        ]
    )

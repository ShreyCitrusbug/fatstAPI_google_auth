"""
Database file contains all database configurations and  connections.
"""

# import libraries
import os

# Third party imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Local imports
from app.settings import settings

# Create database engine
engine = create_engine(
    settings.get_database_string, connect_args={"check_same_thread": False}
)

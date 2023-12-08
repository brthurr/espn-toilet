import os
from dotenv import load_dotenv

# Specify the path to the .env file relative to the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:
    # Flask-related configuration options
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging configuration
    LOG_FILENAME = 'logs/toilet-v2.log'
    LOG_LEVEL = 'INFO'  # Adjust this based on your needs
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"

    # ESPN API configuration
    ESPN_LEAGUE_ID = os.environ.get('LEAGUE_ID')
    ESPN_S2 = os.environ.get('ESPN_S2')
    SWID = os.environ.get('SWID')

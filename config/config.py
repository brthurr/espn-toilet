import os
from dotenv import load_dotenv

# Specify the path to the .env file relative to the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


class Config:
    # Flask-related configuration options
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging configuration
    LOG_FILENAME = "logs/espn-toilet.log"
    LOG_LEVEL = "DEBUG"  # Adjust this based on your needs
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # ESPN API configuration
    ESPN_LEAGUE_ID = os.environ.get("LEAGUE_ID")
    ESPN_S2 = os.environ.get("ESPN_S2")
    SWID = os.environ.get("SWID")

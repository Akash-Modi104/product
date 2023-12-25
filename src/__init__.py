from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from config.log_config import get_logger
from src.database.intialize_database import create_table_not_exits
log = logging.getLogger(__name__)

load_dotenv()


app = Flask(__name__)


def create_app(mode:str):
    get_logger()
    log.info("starting FLASK Application")
    CORS(app)
    DB_USERNAME = os.getenv('DB_USERNAME', 'your_username')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT =os.getenv('DB_PORT', 3606)
    DB_NAME = os.getenv('DB_NAME', 'your_db')
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] =f'mysql+pymysql://{DB_USERNAME}:' \
                                                     f'{DB_PASSWORD}@{DB_HOST}:' \
                                                     f'{DB_PORT}/{DB_NAME}'


        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        create_table_not_exits(app)
        from src.controller import routes_controller
    return app
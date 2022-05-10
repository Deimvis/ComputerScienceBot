import os
from dotenv import load_dotenv
import telebot

load_dotenv('.env')
load_dotenv('.testenv')
BOT_TOKEN = os.getenv('BOT_TOKEN')
FILES_DIR = os.getenv('FILES_DIR')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_CACHE_SIZE = int(os.getenv('DB_CACHE_SIZE'))
DB_CACHE_TTL = int(os.getenv('DB_CACHE_TTL'))
DB_MAX_ROW_COUNT_FOR_CACHE = int(os.getenv('DB_MAX_ROW_COUNT_FOR_CACHE'))
MAX_USERS_ONLINE = int(os.getenv('MAX_USERS_ONLINE'))

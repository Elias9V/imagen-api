import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

DB_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'sslmode': 'require'
}
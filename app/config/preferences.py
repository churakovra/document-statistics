from os import getenv

from dotenv import load_dotenv

#db
load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#backend
BACK_SERVICE_NAME = getenv("BACK_SERVICE_NAME")
BACKEND_PORT = getenv("BACKEND_PORT")

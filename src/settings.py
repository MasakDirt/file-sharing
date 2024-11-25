import os

from dotenv import load_dotenv
from starlette.templating import Jinja2Templates


load_dotenv()


# Get all credentials from .env
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
HOST = os.getenv("HOST")

DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOST}:3306/{MYSQL_DATABASE}"

DEBUG = os.getenv("DEBUG") == "True"

# CSRF
CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY")

# Get important dir paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = Jinja2Templates(directory=TEMPLATES_DIR)

MEDIA_DIR = os.path.join(BASE_DIR, "media")
UPLOADED_DIR = os.path.join(MEDIA_DIR, "uploaded")


# File limitations
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx", ".pptx",
                      ".yaml", ".py", ".xml", ".json"}
MAX_FILE_SIZE = 2 * 1024 * 1024

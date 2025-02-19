from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


PERMISSIONS = {
    "/users/add-role": {
        "GET": ["admin"],
        "POST": ["admin"]
    },
    "/users/remove-role": {
        "GET": ["admin"],
        "POST": ["admin"]
    },
    "/users/": {
        "GET": ["admin"],
        "PUT": ["admin"],
        "DELETE": ["admin"]
    },
    "/users/me": {
        "GET": ["basic_user"]
    },
}
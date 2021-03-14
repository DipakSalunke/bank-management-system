
import os
from datetime import timedelta
DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///user.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False 
PROPAGATE_EXCEPTIONS = True 
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
JWT_BLACKLIST_TOKEN_CHECKS = ["access","refresh"]
ACCESS_EXPIRES = timedelta(hours=1)
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
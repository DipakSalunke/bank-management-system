
import os
from datetime import timedelta
DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///account.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False 
PROPAGATE_EXCEPTIONS = True 
ACCESS_EXPIRES = timedelta(hours=1)
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
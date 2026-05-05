from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
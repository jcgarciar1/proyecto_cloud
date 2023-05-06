import os
from dotenv import load_dotenv

load_dotenv()


OUR_HOST = os.getenv("DB_HOST")
OUR_DB = os.getenv("DB_DB")
OUR_USER = os.getenv("DB_USER")
OUR_PORT = os.getenv("DB_PORT")
OUR_PW = os.getenv("DB_PW")
OUR_SECRET = os.getenv("SECRET")
OUR_JWTSECRET = os.getenv("JWTSECRET")
PROJECT_ID = os.getenv("CLOUD_SQL")

DEBUG = False
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET
SECRET_KEY = OUR_SECRET

MAIL_SERVER = os.getenv("MAIL_SERVER", "sandbox.smtp.mailtrap.io")
MAIL_PORT = os.getenv("MAIL_PORT", 2525)
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "158bc42e00a887")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "ad50ecc9dcaaa8")
MAIL_USE_TLS = True
MAIL_USE_SSL = False

import os


OUR_HOST=os.getenv("DB_HOST", "192.168.1.11")
OUR_DB=os.getenv("DB_DB", "libros")
OUR_USER=os.getenv("DB_USER", "postgres")
OUR_PORT=os.getenv("DB_PORT", "5432")
OUR_PW=os.getenv("DB_PW", "libros")
OUR_SECRET=os.getenv("SECRET", "libros")
OUR_JWTSECRET=os.getenv("JWTSECRET", "libros")

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET
SECRET_KEY = OUR_SECRET

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://192.168.1.11:6379/0")              
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://192.168.1.11:6379/0")
MAIL_SERVER = os.getenv("MAIL_SERVER", "sandbox.smtp.mailtrap.io")
MAIL_PORT = os.getenv("MAIL_PORT", 2525)
MAIL_USERNAME =  os.getenv("MAIL_USERNAME", '158bc42e00a887')
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", 'ad50ecc9dcaaa8')
MAIL_USE_TLS = True
MAIL_USE_SSL = False
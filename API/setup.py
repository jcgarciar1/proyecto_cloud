'''
Setup of the python package for the API 
'''
from setuptools import setup

setup(
    name='back',
    packages=['back'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        "flask-mail",
        'marshmallow-sqlalchemy',
        'flask-restful',
        'flask-marshmallow',
        'flask-jwt-extended',
        'python-dotenv',
        'psycopg2-binary',
        'marshmallow_enum',
        'Flask-CeleryExt'
    ],
)
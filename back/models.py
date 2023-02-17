import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from app import ma, db

'''
Modelos
'''
class Usuario(db.Model):
    usuario = db.Column(db.String(200))
    email = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(100))

    def hashear_clave(self):
        '''
        Hashea la clave en la base de datos
        '''
        self.password = generate_password_hash(self.password, 'sha256')

    def verificar_clave(self, clave):
        '''
        Verifica la clave hasheada con la del parámetro
        '''
        return check_password_hash(self.password, clave)


'''
Schemas
'''
class UsuarioSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("usuario", "email", "password")



usuario_schema = UsuarioSchema()
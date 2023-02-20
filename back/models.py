import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from back import ma, db


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


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(200))
    extension_original = db.Column(db.String(200))
    extension_conversion = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)
    usuario_task = db.Column(db.String(100), db.ForeignKey('usuario.email'), nullable = False)


'''
Schemas
'''
class UsuarioSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("usuario", "email", "password")

class TaskSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("nombre_archivo", "extension_original", "extension_conversion")



usuario_schema = UsuarioSchema()
task_schema = UsuarioSchema()
tasks_schema = UsuarioSchema(many = True)
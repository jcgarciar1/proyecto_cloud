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


class OriginalFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(200))
    extension_conversion = db.Column(db.String(200))
    status = db.Column(db.String(200), default = "Uploaded")
    fecha_creacion = db.Column(db.DateTime(), default = datetime.now)
    usuario_task = db.Column(db.String(100), db.ForeignKey('usuario.email'), nullable = False)


class ConvertedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(200))
    fecha_creacion = db.Column(db.DateTime(), default = datetime.now)
    original_file = db.Column(db.Integer, db.ForeignKey('original_file.id', ondelete = "CASCADE"), nullable = False)
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

class OriginalFileSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("id","nombre_archivo","extension_conversion","status")


class ConvertedFileSchema(ma.Schema):
    '''
    Representa el schema de un admin
    '''
    class Meta:
        fields = ("nombre_archivo", "extension_original", "extension_conversion")



usuario_schema = UsuarioSchema()

original_schema = OriginalFileSchema()
originals_schema = OriginalFileSchema(many = True)

converted_schema = ConvertedFileSchema()
converteds_schema = ConvertedFileSchema(many = True)
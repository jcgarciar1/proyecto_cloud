import os
from datetime import timedelta
from flask import request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_restful import Api

from back import api, db
from back.models import Usuario, OriginalFile, original_schema, ConvertedFile, originals_schema

from back.tasks import convert_zip, convert_targz, convert_tarbz

'''
Recurso que administra el servicio de login
'''
class RecursoLogin(Resource):
    def post(self):
        request.get_json(force=True)
        usuario = Usuario.query.get(request.json['email'])
        
        if usuario is None:
            return {'message':'El email ingresado no está registrado'}, 400
        
        if not usuario.verificar_clave(request.json['password']):
            return {'message': 'Contraseña incorrecta'}, 400
        
        try:
            access_token = create_access_token(identity = request.json['email'], expires_delta = timedelta(days = 1))
            return {
                'message':'Sesion iniciada',
                'access_token':access_token
            }
        
        except:
            return {'message':'Ha ocurrido un error'}, 500
    
'''
Recurso que administra el servicio de registro
'''
class RecursoRegistro(Resource):
    def post(self):
        if Usuario.query.filter_by(email=request.json['email']).first() is not None:
            return {'message': f'El correo({request.json["email"]}) ya está registrado'}, 400
        
        if request.json['email'] == '' or request.json['password'] == '' or request.json['usuario'] == '':
            return {'message': 'Campos invalidos'}, 400
        
        nuevo_usuario = Usuario(
            email = request.json['email'],
            password = request.json['password'],
            usuario = request.json['usuario'],
        )
        
        nuevo_usuario.hashear_clave()

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            access_token = create_access_token(identity = request.json['email'], expires_delta = timedelta(days = 1))
            return {
                'message': f'El correo {request.json["email"]} ha sido registrado',
                'access_token': access_token 
            }

        except:
            return {'message':'Ha ocurrido un error'}, 500


   
'''
Recurso que administra el servicio de tasks
'''
class RecursoTasks(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()  
        tasks = OriginalFile.query.filter_by(usuario_task = email).all()        
        return originals_schema.dump(tasks) 
          
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        file = request.files['file']
        nombre = file.filename
        conversion = request.form['convertir']
        
        nueva_libro = OriginalFile(
            nombre_archivo = nombre,
            extension_conversion = conversion,
            data = file.read(),
            usuario_task = email
            )
        db.session.add(nueva_libro)
        db.session.commit()

        if conversion == "zip":
            convert_zip.delay(nueva_libro.id,email)
        elif conversion == "targz":
            convert_targz.delay(nueva_libro.id,email)
        elif conversion == "tarbz2":
            convert_tarbz.delay(nueva_libro.id,email)


        return original_schema.dump(nueva_libro)

  
'''
Recurso que administra el servicio de un task (Detail)
'''
class RecursoMiTask(Resource):
    @jwt_required()
    def get(self, id_task):
        email = get_jwt_identity()
        task = OriginalFile.query.get_or_404(id_task)

        if task.usuario_task != email:
            return {'message':'No tiene acceso a esta publicación'}, 401
        else:
            return original_schema.dump(task)


    @jwt_required()
    def delete(self, id_task):
        email = get_jwt_identity()
        libro = OriginalFile.query.get_or_404(id_task)
        
        if libro.usuario_task != email:
            return {'message':'No tiene acceso a esta publicación'}, 401

        if libro.status != "Processed":
            return {'message':'El archivo no ha sido procesado'}, 400
        
        db.session.delete(libro)
        db.session.commit()        
        return '', 204


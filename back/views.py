import os
from datetime import timedelta
from flask import request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_restful import Api

from back import api, db
from back.models import Usuario, task_schema, tasks_schema, Task

from back.tasks import add

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
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type = int, help='El limite no puede ser convertido')
        parser.add_argument('order')
        args = parser.parse_args()
        
        if args['order'] == '0':
            tasks = Task.query.filter_by(usuario_libro = email).order_by(db.desc(Task.id)).limit(args['limit']).all()
        else:
            tasks = Task.query.filter_by(usuario_libro = email).order_by(db.asc(Task.id)).limit(args['limit']).all()

        
        return tasks_schema.dump(tasks) 
          
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        file = request.files['file']
        archivo_split = file.filename.split(".")
        nombre = archivo_split[0]
        extension = archivo_split[1]
        
        nueva_libro = Task(
            nombre_archivo = nombre,
            extension_original = extension,
            extension_conversion = request.form['convertir'],
            data = file.read(),
            usuario_task = email
            )
        db.session.add(nueva_libro)
        db.session.commit()

        for i in range(10000):
            add.delay(i, i)

        return task_schema.dump(nueva_libro)


import os
from datetime import timedelta
from flask import request, current_app, send_from_directory, send_file
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    JWTManager,
)
from flask_restful import Api
import requests
from back import api, db
from back.models import (
    Usuario,
    OriginalFile,
    original_schema,
    ConvertedFile,
    originals_schema,
    converted_schema,
)
from werkzeug.utils import secure_filename
import io
from google.cloud import storage, pubsub_v1
from flask import after_this_request


client = storage.Client(project="cloud-project-382023")
bucket = client.get_bucket("compression_app_files")


publisher = pubsub_v1.PublisherClient()
topic_path = "projects/cloud-project-382023/topics/compresiones"


"""
Recurso que administra el servicio de login
"""


class RecursoLogin(Resource):
    def post(self):
        request.get_json(force=True)
        usuario = Usuario.query.get(request.json["email"])

        if usuario is None:
            return {"message": "El email ingresado no está registrado"}, 400

        if not usuario.verificar_clave(request.json["password"]):
            return {"message": "Contraseña incorrecta"}, 400

        try:
            access_token = create_access_token(
                identity=request.json["email"], expires_delta=timedelta(days=1)
            )
            return {"message": "Sesion iniciada", "access_token": access_token}

        except:
            return {"message": "Ha ocurrido un error"}, 500


"""
Recurso que administra el servicio de registro
"""


class RecursoRegistro(Resource):
    def post(self):
        if Usuario.query.filter_by(email=request.json["email"]).first() is not None:
            return {
                "message": f'El correo({request.json["email"]}) ya está registrado'
            }, 400

        if (
            request.json["email"] == ""
            or request.json["password1"] == ""
            or request.json["password2"] == ""
            or request.json["usuario"] == ""
        ):
            return {"message": "Campos invalidos"}, 400

        passwd1 = request.json["password1"]
        passwd2 = request.json["password2"]

        if passwd1 != passwd2:
            return {"message": "Las contraseñas no coinciden"}, 400

        nuevo_usuario = Usuario(
            email=request.json["email"],
            password=passwd1,
            usuario=request.json["usuario"],
        )

        nuevo_usuario.hashear_clave()

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            access_token = create_access_token(
                identity=request.json["email"], expires_delta=timedelta(days=1)
            )
            return {
                "message": f'El correo {request.json["email"]} ha sido registrado',
                "access_token": access_token,
            }

        except:
            return {"message": "Ha ocurrido un error"}, 500


"""
Recurso que administra el servicio de tasks
"""


class RecursoTasks(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            parser = reqparse.RequestParser()
            parser.add_argument(
                "max", type=int, help="El limite no puede ser convertido"
            )
            parser.add_argument("order")
            args = parser.parse_args()
            if args["order"] == "0":
                tasks = (
                    OriginalFile.query.filter_by(usuario_task=email)
                    .order_by(db.desc(OriginalFile.id))
                    .limit(args["max"])
                    .all()
                )
            else:
                tasks = (
                    OriginalFile.query.filter_by(usuario_task=email)
                    .order_by(db.asc(OriginalFile.id))
                    .limit(args["max"])
                    .all()
                )

        except Exception as e:
            tasks = (
                OriginalFile.query.filter_by(usuario_task=email)
                .order_by(db.desc(OriginalFile.id))
                .all()
            )

        return originals_schema.dump(tasks)

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        file = request.files["fileName"]
        nombre = file.filename
        conversion = request.form["newFormat"]
        nuevo_task = OriginalFile(
            nombre_archivo=nombre, extension_conversion=conversion, usuario_task=email
        )

        stream = io.BytesIO(file.read())
        # Create a blob object from the filepath
        blob = bucket.blob(f"original_files/{email}/{nombre}")
        blob.upload_from_file(stream)

        data = "Nuevo archivo para comprimir"
        data = data.encode("utf-8")
        

        # Upload the file to a destination
        db.session.add(nuevo_task)
        db.session.commit()
        print(nuevo_task.id)
        future = publisher.publish(
            topic_path, data, email=email, filename=nombre, conversion=conversion, id = str(nuevo_task.id)
        )

        return original_schema.dump(nuevo_task)


"""
Recurso que administra el servicio de un task (Detail)
"""


class RecursoMiTask(Resource):
    @jwt_required()
    def get(self, id_task):
        email = get_jwt_identity()
        task = OriginalFile.query.get_or_404(id_task)

        if task.usuario_task != email:
            return {"message": "No tiene acceso a esta publicación"}, 401
        else:
            return original_schema.dump(task)

    @jwt_required()
    def delete(self, id_task):
        email = get_jwt_identity()
        task = OriginalFile.query.get_or_404(id_task)

        if task.usuario_task != email:
            return {"message": "No tiene acceso a esta publicación"}, 401

        if task.status != "Processed":
            return {"message": "El archivo no ha sido procesado"}, 400
        

        procesado = task.nombre_archivo.split(".")[0] + "." + task.extension_conversion
        blob = bucket.blob(f"converted_files/{email}/{procesado}")
        blob.delete()

        blob2 = bucket.blob(f"original_files/{email}/{task.nombre_archivo}")        
        blob2.delete()

        db.session.delete(task)
        db.session.commit()

        return "", 204


"""
Recurso que administra la descarga de un task
"""
class RecursoDescargaTask(Resource):
    @jwt_required()
    def get(self, id_task):
        email = get_jwt_identity()
        task = OriginalFile.query.get_or_404(id_task)

        if task.usuario_task != email:
            return {"message": "No tiene acceso a esta publicación"}, 401
        else:
            
            if task.status == "Processed":
                procesado = task.nombre_archivo.split(".")[0] + "." + task.extension_conversion
                blob = bucket.blob(f"converted_files/{email}/{procesado}")
                blob.download_to_filename(f"back/processed_files/{procesado}")
                @after_this_request
                def delete(response):
                    os.remove(f"back/processed_files/{procesado}")
                    return response
                return send_file(
                   f"processed_files/{procesado}",
                    download_name=procesado,
                    as_attachment=True,
                )
            else:
                blob = bucket.blob(f"original_files/{email}/{task.nombre_archivo}")
                blob.download_to_filename(f"back/original_files/{task.nombre_archivo}")
                @after_this_request
                def delete(response):
                    os.remove(f"back/original_files/{task.nombre_archivo}")
                    return response
                return send_file(
                   f"original_files/{task.nombre_archivo}",
                    download_name=task.nombre_archivo,
                    as_attachment=True,
                )
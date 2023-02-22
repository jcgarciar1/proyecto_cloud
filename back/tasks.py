from celery import shared_task
from back import db,mail
from back.models import ConvertedFile, OriginalFile
from flask_mail import Message
import tarfile
import gzip
import bz2
import io
import zipfile
import os

@shared_task
def convert_zip(name,correo):
        original = OriginalFile.query.get_or_404(name)
        file = original.data
        without_extension = original.nombre_archivo.split(".")[0]
        original_path = f"back/temp/{original.nombre_archivo}"
        converted_path = f"back/temp/{without_extension}.zip"

        with open(original_path, 'wb') as archivo_original:
                archivo_original.write(file)
        archivo_original.close()

        with zipfile.ZipFile(converted_path, mode="w") as archive:
                archive.write(original_path)
        archive.close()

        with open(converted_path, 'rb') as zipFile:
                convertido = ConvertedFile(
                        nombre_archivo = without_extension + ".zip",
                        data = zipFile.read(),
                        original_file = name,
                        usuario_task = correo
                )
        zipFile.close()
        db.session.add(convertido)
        db.session.commit()
        original.status = "Processed"
        db.session.commit()

        msg = Message('Compresión lista!', sender =   'noreply@compresionesinc.com', recipients = [correo])
        msg.body = f"Hola, tu archivo {original.nombre_archivo} ya comprimido en formato zip y está disponible para descargar"
        mail.send(msg)

        os.remove(original_path)
        os.remove(converted_path)

@shared_task
def convert_targz(name,correo):
        original = OriginalFile.query.get_or_404(name)
        file = original.data
        without_extension = original.nombre_archivo.split(".")[0]
        original_path = f"back/temp/{original.nombre_archivo}"
        converted_path = f"back/temp/{without_extension}.tar.gz"

        with open(original_path, 'wb') as archivo_original:
                archivo_original.write(file)
        archivo_original.close()

        tar = tarfile.open(converted_path, 'w:gz')
        tar.add(original_path)
        tar.close()

        with open(converted_path, 'rb') as tar:
                convertido = ConvertedFile(
                        nombre_archivo = without_extension + ".tar.gz",
                        data = tar.read(),
                        original_file = name,
                        usuario_task = correo
                )
        tar.close()
        db.session.add(convertido)
        db.session.commit()
        original.status = "Processed"
        db.session.commit()

        msg = Message('Compresión lista!', sender =   'noreply@compresionesinc.com', recipients = [correo])
        msg.body = f"Hola, tu archivo {original.nombre_archivo} ya comprimido en formato tar.gz y está disponible para descargar"
        mail.send(msg)


        os.remove(original_path)
        os.remove(converted_path)

@shared_task
def convert_tarbz(name,correo):
        original = OriginalFile.query.get_or_404(name)
        file = original.data
        without_extension = original.nombre_archivo.split(".")[0]
        original_path = f"back/temp/{original.nombre_archivo}"
        converted_path = f"back/temp/{without_extension}.tar.bz2"

        with open(original_path, 'wb') as archivo_original:
                archivo_original.write(file)
        archivo_original.close()

        tar = tarfile.open(converted_path, 'w:bz2')
        tar.add(original_path)
        tar.close()

        with open(converted_path, 'rb') as tar:
                convertido = ConvertedFile(
                        nombre_archivo = without_extension + ".tar.bz2",
                        data = tar.read(),
                        original_file = name,
                        usuario_task = correo
                )
        tar.close()
        db.session.add(convertido)
        db.session.commit()
        original.status = "Processed"
        db.session.commit()

        msg = Message('Compresión lista!', sender =   'noreply@compresionesinc.com', recipients = [correo])
        msg.body = f"Hola, tu archivo {original.nombre_archivo} ya comprimido en formato tar.bz2 y está disponible para descargar"
        mail.send(msg)


        os.remove(original_path)
        os.remove(converted_path)
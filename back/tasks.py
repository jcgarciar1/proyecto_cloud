from celery import shared_task
from back import db
from back.models import ConvertedFile, OriginalFile
import tarfile
import gzip
import bz2
import io


@shared_task
def convert_zip(name,correo):
        original = OriginalFile.query.get_or_404(name)
        file = original.data
        without_extension = original.nombre_archivo.split(".")[0]
        with open(f"/Users/juangarcia/Downloads/proyecto_cloud/back/temp/{without_extension}.zip", 'wb') as zipFile:
                zipFile.write(file)
        zipFile.close()
        with open(f"/Users/juangarcia/Downloads/proyecto_cloud/back/temp/{without_extension}.zip", 'rb') as zipFile:
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

@shared_task
def convert_targz(name,correo):
        original = OriginalFile.query.get_or_404(name)
        file = original.data
        without_extension = original.nombre_archivo.split(".")[0]

        with tarfile.open(f"/Users/juangarcia/Downloads/proyecto_cloud/back/temp/{without_extension}.tar.gz", mode='w:gz') as tar:
                tarinfo = tarfile.TarInfo(name)
                tar.addfile(tarinfo, file)
        tar.close()
        with open(f"/Users/juangarcia/Downloads/proyecto_cloud/back/temp/{without_extension}.tar.gz", 'rb') as tar:
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

@shared_task
def convert_tarbz(name,correo):
        original = OriginalFile.query.get_or_404(name)
        file = original.data
        without_extension = original.nombre_archivo.split(".")[0]

        with tarfile.open(f"/Users/juangarcia/Downloads/proyecto_cloud/back/temp/{without_extension}.tar.bz2", mode='w:bz2') as tar:
                tarinfo = tarfile.TarInfo(name)
                tar.addfile(tarinfo, file)
        tar.close()
        with open(f"/Users/juangarcia/Downloads/proyecto_cloud/back/temp/{without_extension}.tar.bz2", 'rb') as tar:
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
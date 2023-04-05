from celery import Celery
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy import create_engine, MetaData,Table, Column, Numeric, Integer, VARCHAR, update
import zipfile
import tarfile

app = Celery( 'tasks' , broker = 'redis://10.128.0.5:6379/0' )

engine = create_engine('postgresql+psycopg2://postgres:libros@10.128.0.3:5432/libros')
# initialize the Metadata Object
meta = MetaData(bind=engine)
MetaData.reflect(meta)
# Get the `books` table from the Metadata object
ORIGINAL = meta.tables['original_file']


@app.task
def convert_zip(id,email,filename):
    original_path = f"/compressed/{email}/{filename}"
    without_extension = filename.split(".")[0]
    converted_path =f"/processed_files/{email}/{without_extension}"+ ".zip"

    with zipfile.ZipFile(converted_path, mode="w") as archive:
        archive.write(original_path)
    archive.close()

    u = update(ORIGINAL)
    u = u.values({"status": "Processed"})
    u = u.where(ORIGINAL.c.id == id)
    engine.execute(u)

    return f"Processed {original_path}"

@app.task
def convert_tar(id,email,filename):
    original_path = f"/compressed/{email}/{filename}"
    without_extension = filename.split(".")[0]
    converted_path =f"/processed_files/{email}/{without_extension}"+ ".tar.gz"

    tar = tarfile.open(converted_path, 'w:gz')
    tar.add(original_path)
    tar.close()

    u = update(ORIGINAL)
    u = u.values({"status": "Processed"})
    u = u.where(ORIGINAL.c.id == id)
    engine.execute(u)

    return f"Processed {original_path}"

@app.task
def convert_tarbz(id,email,filename):
    original_path = f"/compressed/{email}/{filename}"
    without_extension = filename.split(".")[0]
    converted_path =f"/processed_files/{email}/{without_extension}"+ ".tar.bz2"

    tar = tarfile.open(converted_path, 'w:bz2')
    tar.add(original_path)
    tar.close()


    u = update(ORIGINAL)
    u = u.values({"status": "Processed"})
    u = u.where(ORIGINAL.c.id == id)
    engine.execute(u)

    return f"Processed {original_path}"
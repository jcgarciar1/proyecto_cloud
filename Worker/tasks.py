from google.cloud import storage,pubsub_v1
import os
import tempfile
import zipfile
import tarfile
import io


client = storage.Client(project="cloud-project-382023")
bucket = client.get_bucket("compression_app_files")


def gz(temp,filename,message,email):
    try:
        blob = bucket.get_blob(f'original_files/{email}/{filename}')
        blob = blob.download_as_bytes()

        with open(f"/tmp/{filename}","wb") as original:
            original.write(blob)
        original.close()
        with tarfile.open(fileobj = temp, mode="w:gz") as archive:
            archive.add(f"/tmp/{filename}")
        archive.close()
    finally:
        temp.seek(0)
        stream = io.BytesIO(temp.read())
        blob2 = bucket.blob(f"converted_files/{email}/{temp.name}")
        blob2.upload_from_file(stream)
        temp.close()

def zip_file(temp,filename,message,email):
    try:
        blob = bucket.get_blob(f'original_files/{email}/{filename}')
        blob = blob.download_as_bytes()
        with zipfile.ZipFile(temp, mode="w") as archive:
            archive.writestr(filename,blob)
        archive.close()
    finally:
        temp.seek(0)
        stream = io.BytesIO(temp.read())
        blob2 = bucket.blob(f"converted_files/{email}/{temp.name}")
        blob2.upload_from_file(stream)
        temp.close()



def tar(temp,filename,message,email):
    try:
        blob = bucket.get_blob(f'original_files/{email}/{filename}')
        blob = blob.download_as_bytes()

        with open(f"/tmp/{filename}","wb") as original:
            original.write(blob)
        original.close()
        with tarfile.open(fileobj = temp, mode="w:bz2") as archive:
            archive.add(f"/tmp/{filename}")
        archive.close()
    finally:
        temp.seek(0)
        stream = io.BytesIO(temp.read())
        blob2 = bucket.blob(f"converted_files/{email}/{temp.name}")
        blob2.upload_from_file(stream)
        temp.close()

def callback(message, context):
    conversion = message["attributes"]["conversion"]
    without_extension = message["attributes"]["filename"].split(".")[0]
    temp = tempfile.NamedTemporaryFile()
    temp.name = f"{without_extension}.{conversion}"
    filename = message["attributes"]["filename"]
    email = message["attributes"]["email"]

    if conversion == "zip":
        zip_file(temp,filename,message,email)
    elif conversion == "tar.gz":
        gz(temp,filename,message,email)
    elif conversion == "tar.bz2":
        tar(temp,filename,message,email)
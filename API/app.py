from back import create_app, ext_celery

app = create_app()
celery = ext_celery.celery
app.app_context().push()
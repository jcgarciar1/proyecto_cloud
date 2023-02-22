from back import api
from back.views import RecursoRegistro, RecursoLogin, RecursoTasks, RecursoMiTask, RecursoDescargaTask

api.add_resource(RecursoTasks, '/api/tasks')
api.add_resource(RecursoRegistro, '/api/auth/registro')
api.add_resource(RecursoLogin, '/api/auth/login')
api.add_resource(RecursoMiTask, '/api/tasks/<int:id_task>')
api.add_resource(RecursoDescargaTask, '/api/files/<int:id_task>')


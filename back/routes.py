from app import api
from views import RecursoRegistro, RecursoLogin
#, RecursoTarjeta, RecursoTarjetas

api.add_resource(RecursoRegistro, '/api/auth/registro')
api.add_resource(RecursoLogin, '/api/auth/login')

# /api/reviews?limit=num_post&order=desc|asc
# api.add_resource(RecursoLibros, '/api/reviews')

#api.add_resource(RecursoLibros, '/api/libros')
#api.add_resource(RecursoMiLibro, '/api/libros/<string:id_libro>')

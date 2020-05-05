#from apps.proyecto.models import Proyecto, Tipo_metodologia
import apps.usuarios.models
#from apps.scrum.models import Scrum, Pbacklog, HistoriaUsuario, Sbacklog

from apps import Session

session = Session()

usuarios = session.query(apps.usuarios.models.Usuario).all()


print('\n### All usuarios:')

for u in usuarios:
    print({u.nombre})
from apps.proyecto.models import Rol

def verificar_roles(nombre, metodologia):
    try:
        rol = Rol.objects.get(nombre=nombre)
        return rol
    except:
        if metodologia.nombre == "SCRUM":            
            Rol.objects.create(nombre="Scrum Master", metodologia=metodologia)
            Rol.objects.create(nombre="Development Team", metodologia=metodologia)
            Rol.objects.create(nombre="Asesor", metodologia=metodologia)

            rol = Rol.objects.create(nombre=nombre, metodologia=metodologia)
            return rol
        elif metodologia.nombre == "XP":
            rol = Rol.objects.create(nombre=nombre, metodologia=metodologia)

            Rol.objects.create(nombre="Coach", metodologia=metodologia)
            Rol.objects.create(nombre="Testers", metodologia=metodologia)
            Rol.objects.create(nombre="Programador", metodologia=metodologia)
            Rol.objects.create(nombre="Asesor", metodologia=metodologia)
            return rol
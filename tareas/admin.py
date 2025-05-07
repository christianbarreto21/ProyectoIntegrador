from django.contrib import admin
from .models import AuditoriaEvento, RegistroResiduo, Rol, Ubicacion, Usuario, Empresa, Evento

admin.site.register(Rol)

admin.site.register(Usuario)
admin.site.register(Ubicacion)
admin.site.register(AuditoriaEvento)
admin.site.register(Empresa)
admin.site.register(Evento)
admin.site.register(RegistroResiduo)
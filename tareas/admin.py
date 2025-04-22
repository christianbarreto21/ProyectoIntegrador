from django.contrib import admin
from .models import AuditoriaEvento, Rol, Ubicacion, Usuario

admin.site.register(Rol)

admin.site.register(Usuario)
admin.site.register(Ubicacion)
admin.site.register(AuditoriaEvento)



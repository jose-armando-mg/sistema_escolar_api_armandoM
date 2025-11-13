# En dev_sistema_escolar_api/admin.py (VERSION CORREGIDA, ASUMIENDO QUE USAS DECORADORES)

from django.contrib import admin
from dev_sistema_escolar_api.models import *

# Opción 1: Administradores (usando decorador)
@admin.register(Administradores)
class AdministradoresAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

# Opción 2: Alumnos (usando decorador)
@admin.register(Alumnos)
class AlumnosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

# Opción 3: Maestros (usando decorador)
@admin.register(Maestros)
class MaestrosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

# Asegúrate de que NO existan estas líneas al final:
# admin.site.register(Administradores, ProfilesAdmin)
# admin.site.register(Alumnos, ProfilesAdmin)
# admin.site.register(Maestros, ProfilesAdmin)
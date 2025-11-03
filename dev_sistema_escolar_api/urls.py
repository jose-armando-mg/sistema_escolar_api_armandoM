from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dev_sistema_escolar_api.views.alumnos import AlumnoView
from dev_sistema_escolar_api.views.maestros import MaestroView
from dev_sistema_escolar_api.views.users import AdminView
from .views.bootstrap import VersionView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/version/", VersionView.as_view(), name="api-version"),
    path("api/admin/", AdminView.as_view(), name="admin-register"),
    path ("api/alumno/", AlumnoView.as_view(), name="alumno-register"),
    path("api/maestro/", MaestroView.as_view(), name="maestro-register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


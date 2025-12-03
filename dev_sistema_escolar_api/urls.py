from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dev_sistema_escolar_api.views.eventos import EventoView, EventosAll, TotalEventos
from .views.bootstrap import VersionView
from dev_sistema_escolar_api.views import bootstrap
from dev_sistema_escolar_api.views import users
from dev_sistema_escolar_api.views import alumnos
from dev_sistema_escolar_api.views import maestros
from dev_sistema_escolar_api.views import auth

urlpatterns = [
   #Create Admin
        path('admin/', users.AdminView.as_view()),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Edit Admin
        #path('admins-edit/', users.AdminsViewEdit.as_view())
    #Create Alumno
        path('alumnos/', alumnos.AlumnoView.as_view()),
    #Create Maestro
        path('maestros/', maestros.MaestroView.as_view()),
        path('maestros/<int:id>/', maestros.MaestroView.as_view()),
    #Maestro Data
        path('lista-maestros/', maestros.MaestrosAll.as_view()),
    #Aumno data
        path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Login
        path('token/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()), 

        path('eventos/', EventoView.as_view()),        # POST crear, GET por id, PUT actualizar, DELETE
        
        path('lista-eventos/', EventosAll.as_view()),
       
        #Total Users
        path('total-usuarios/', users.TotalUsers.as_view()), 
       
        path('total-eventos/', TotalEventos.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
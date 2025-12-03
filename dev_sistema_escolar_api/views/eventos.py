from django.db.models import *
from django.db import transaction
from dev_sistema_escolar_api.serializers import *
from dev_sistema_escolar_api.models import *
import json
import logging
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User

class EventosAll(generics.CreateAPIView):
    # Obtener todos los eventos académicos
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        eventos = EventoAcademico.objects.all().order_by("-id")
        lista = EventoAcademicoSerializer(eventos, many=True).data
        return Response(lista, 200)


class EventoView(generics.CreateAPIView):
    serializer_class = EventoAcademicoSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación

    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(EventoAcademico, id=request.GET.get("id"))
        evento = EventoAcademicoSerializer(evento, many=False).data
        return Response(evento, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el responsable - puede ser Maestro o Admin
            responsable_id = request.data.get('responsable_id')
            responsable = None
            
            if responsable_id:
                # Intentar obtener como Maestro primero
                try:
                    maestro = Maestros.objects.get(id=responsable_id)
                    responsable = maestro.user
                except Maestros.DoesNotExist:
                    # Si no es maestro, intentar como Admin
                    try:
                        admin = Administradores.objects.get(id=responsable_id)
                        responsable = admin.user
                    except Administradores.DoesNotExist:
                        return Response(
                            {"message": "El responsable especificado no existe"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            else:
                return Response(
                    {"message": "El responsable es requerido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear el evento con el User asociado
            evento = EventoAcademico.objects.create(
                nombre=request.data.get('nombre'),
                tipo=request.data.get('tipo'),
                fecha=request.data.get('fecha'),
                hora_inicio=request.data.get('hora_inicio'),
                hora_fin=request.data.get('hora_fin'),
                lugar=request.data.get('lugar'),
                publico_objetivo=request.data.get('publico_objetivo'),
                programa_educativo=request.data.get('programa_educativo'),
                responsable=responsable,
                descripcion=request.data.get('descripcion'),
                cupo_maximo=request.data.get('cupo_maximo')
            )

            evento.save()

            return Response({"evento_created_id": evento.id}, 201)

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Actualizar evento
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        evento = get_object_or_404(EventoAcademico, id=request.data.get("id"))

        # Validar responsable si se proporciona
        responsable_id = request.data.get('responsable_id')
        if responsable_id:
            responsable = get_object_or_404(User, id=responsable_id)
            evento.responsable = responsable

        # Actualizar campos
        evento.nombre = request.data.get('nombre', evento.nombre)
        evento.tipo = request.data.get('tipo', evento.tipo)
        evento.fecha = request.data.get('fecha', evento.fecha)
        evento.hora_inicio = request.data.get('hora_inicio', evento.hora_inicio)
        evento.hora_fin = request.data.get('hora_fin', evento.hora_fin)
        evento.lugar = request.data.get('lugar', evento.lugar)
        evento.publico_objetivo = request.data.get('publico_objetivo', evento.publico_objetivo)
        evento.programa_educativo = request.data.get('programa_educativo', evento.programa_educativo)
        evento.descripcion = request.data.get('descripcion', evento.descripcion)
        evento.cupo_maximo = request.data.get('cupo_maximo', evento.cupo_maximo)
        evento.save()

        return Response({"evento_updated_id": evento.id}, 200)

    # Eliminar evento
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(EventoAcademico, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details": "Evento eliminado"}, 200)
        except Exception as e:
            return Response({"details": "Error al eliminar: " + str(e)}, 400)
        

class TotalEventos(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            # Agrupar por tipo y contar
            totals = EventoAcademico.objects.values('tipo').annotate(total=Count('id'))

            result = {
                'conferencia': 0,
                'taller': 0,
                'seminario': 0,
                'concurso': 0
            }

            # Normalizar y mapear cada fila a la clave correspondiente
            for row in totals:
                tipo_raw = (row.get('tipo') or '').strip().lower()
                count = int(row.get('total') or 0)

                if not tipo_raw:
                    continue

                if 'confer' in tipo_raw or 'conference' in tipo_raw:
                    result['conferencia'] += count
                elif 'taller' in tipo_raw or 'workshop' in tipo_raw:
                    result['taller'] += count
                elif 'semin' in tipo_raw or 'seminar' in tipo_raw:
                    result['seminario'] += count
                elif 'concurs' in tipo_raw or 'contest' in tipo_raw:
                    result['concurso'] += count
                else:

                    pass

            return Response(result, status=200)

        except Exception as e:
            # registra el error y retorna 500
            try:
                logging.getLogger(__name__).exception("Error calculando totales de eventos")
            except Exception:
                pass
            return Response({'detail': 'Error interno al calcular totales'}, status=500)
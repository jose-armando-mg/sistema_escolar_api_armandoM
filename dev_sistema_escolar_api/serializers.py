from django.contrib.auth.models import User
from rest_framework import serializers
from dev_sistema_escolar_api.models import *

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Intentar autenticar con username o email
        user = None
        if '@' in username:  # Si contiene @, es email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                user = None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = '__all__'

class MaestroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class EventoAcademicoSerializer(serializers.ModelSerializer):
    responsable = UserSerializer(read_only=True)
    
    class Meta:
        model = EventoAcademico
        fields = '__all__'
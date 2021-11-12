from django.db.models import fields
from rest_framework import serializers
from UsuarioApp.models.usuario import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'usu_nombreUsuario', 'password', 'usu_nombre']
    
    def create(self, validated_data):
        userInstance = User.objects.create(**validated_data)
        return userInstance
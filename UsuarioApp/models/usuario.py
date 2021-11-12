from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, usu_nombreUsuario, password=None):
        if not usu_nombreUsuario:
            raise ValueError('User must have an username')
        usuario = self.model(usu_nombreUsuario=usu_nombreUsuario)
        usuario.set_password(password)
        usuario.save(usign=self._db)
        return usuario
    
    def create_superuser(self, usu_nombreUsuario, password):
        usuario = self.create_user(
            usu_nombreUsuario=usu_nombreUsuario,
            password=password,
        )
        usuario.is_admin = True
        usuario.save(usign=self.db)
        return usuario

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigIntegerField('Identificación',primary_key=True, null=False)
    usu_nombreUsuario = models.CharField('Nombre usuario', max_length=60, null=False, blank=False, unique=True)
    password = models.CharField('Contraseña', max_length=256, null=False)
    usu_nombre = models.CharField('Nombre y apellido', max_length=20, null=False)

    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)
    
    objects = UserManager()
    USERNAME_FIELD = 'usu_nombreUsuario'
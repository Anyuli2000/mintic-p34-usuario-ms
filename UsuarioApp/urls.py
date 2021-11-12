from django.db.models import base
from rest_framework import routers, urlpatterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

from .views.usuarioView import CrearUsuarioViewSet
from .views.verifyTokenView import VerifyTokenView

urlpatterns = [
    #url para usuario
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('api/verifyToken/', VerifyTokenView.as_view()),
    path('api/usuario/registro/', CrearUsuarioViewSet.as_view()), #crea el usuario
    #path('api/usuario/<int:pk>/', DetalleUsuarioView.as_view()), #ver los datos del usuario de manera individual
    path('api/usuario/editar/<int:pk>/', CrearUsuarioViewSet.as_view()), #edita la informacion de usuario
    path('api/usuario/eliminar/<int:pk>/', CrearUsuarioViewSet.as_view()), #elimina el usuario
]
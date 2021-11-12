from warnings import catch_warnings
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework import serializers, status, viewsets, views, generics
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated
import json
#from TourApp.utils.correos import send_email #importo para el envio de correos

#models
from UsuarioApp.models.usuario import User
from UsuarioApp.serializers.usuarioSerializer import UsuarioSerializer

class CrearUsuarioViewSet(views.APIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            tokenData = {"usu_nombreUsuario":request.data["usu_nombreUsuario"],
                    "password":request.data["password"]}
            tokenSerializer = TokenObtainPairSerializer(data=tokenData)
            tokenSerializer.is_valid(raise_exception=True)
            return Response(tokenSerializer.validated_data, status=status.HTTP_201_CREATED)
        except:
            errordata = {'detalle': 'La identificacion o el usuario ya existe.'}
            return Response(status=status.HTTP_409_CONFLICT)

    def put(self, request, pk, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != pk:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        jd = json.loads(request.body) #cargamos los datos del usuario por medio de un json
        print(jd) #muestro tal informacion
        usuarios = list(User.objects.filter(id=pk).values()) #verifico si existen usuarios
        if len(usuarios) > 0:
            usuario = User.objects.get(id=pk) #obtengo los datos del usuario mediante su id
            #cargo los campos los cuales se van a modificar
            usuario.usu_nombre = jd['usu_nombre']
            
            usuario.save() #por ultimo los guarda y muestra un success
            datos = {'message':'Success'}
            return Response(datos, status=status.HTTP_200_OK)
        else:
            datos = {'message':'Error'}
            return Response(datos, status=status.HTTP_500_INTERNAL_SERVER_ERROR) #en caso de que el metodo no funcione
    
    def delete(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != pk:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        usuarios = list(User.objects.filter(id=pk).values()) #verifico que si existen usuarios en la tabla
        if len(usuarios) > 0: #si la cantidad es mayor a cero
            User.objects.filter(id=pk).delete() #busca el usuario deacuerdo a su id
            datos = {'message':'Usuario eliminado'} #en caso de que exista lo elimina
            return Response(datos, status=status.HTTP_200_OK)# y devuelve un estado de que a funcionado el metodo
        else:
            datos = {'message':'Usuarios no encontrados'} #de lo contrario muestra este mensaje
            return Response(datos, status=status.HTTP_404_NOT_FOUND) # seguido de enviar un not found

"""class DetalleUsuarioView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)"""

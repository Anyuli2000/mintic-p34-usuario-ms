from django.contrib import admin
from .models.usuario import User

# registro los modelos
admin.site.register(User)
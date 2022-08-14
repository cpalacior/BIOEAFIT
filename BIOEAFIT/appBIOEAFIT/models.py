from contextlib import nullcontext
from django.db import models

# Create your models here.
class TipoUsuario(models.Model):
    idtipousuario = models.SmallIntegerField(primary_key=True)
    desctipousuario = models.CharField(max_length=20)

class Usuario(models.Model):
    identificacion = models.BigIntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=45, unique=False, null=False)
    correo = models.CharField(max_length=45, null=False)
    clave = models.CharField(max_length=30, null=False, unique=False)
    direccion = models.CharField(max_length=50, null=False, unique=False)
    edad = models.SmallIntegerField(null=False, unique=False)
    telefono = models.BigIntegerField(null=False, unique=False)
    idtipousuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

class Bonificacion(models.Model):
    idbonificacion = models.AutoField(primary_key=True, null=False)
    nombre= models.CharField(max_length=30,null=False)
    valor = models.IntegerField(null=False, unique=False)
    cantidad = models.IntegerField(null=False, unique=False)

class Usuario_Bonificacion(models.Model):
    identificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idbonificacion = models.ForeignKey(Bonificacion, on_delete=models.CASCADE)

class Puntos_Usuarios(models.Model):
    identificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)

class Botella(models.Model):
    idbotella =models.AutoField(primary_key=True)
    tamanio = models.IntegerField(null=False)
    peso= models.IntegerField(null=False)
    calidad = models.SmallIntegerField

class Usuario_Botella(models.Model):
    identificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idbotella = models.ForeignKey(Botella, on_delete=models.CASCADE)
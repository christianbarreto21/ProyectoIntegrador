from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
# Modelo para Profesores
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class UsuarioResiduos(models.Model):
    nombre = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios_residuos')

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    # Relación con UsuarioResiduos
    usuario_residuos = models.OneToOneField(
        UsuarioResiduos, 
        on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name='usuario'
    )

    # Solución al conflicto de grupos y permisos
    groups = models.ManyToManyField(Group, related_name="usuario_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuario_permissions", blank=True)

    def __str__(self):
        return self.username


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    categoria  = models.CharField(max_length=100)
    def _str_(self):
        return self.nombre 

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=250)
    fecha = models.DateField()
    hora = models.TimeField()

    def _str_(self):
    
        return self.nombre
class AuditoriaEvento(models.Model):
    evento_id = models.IntegerField()
    operacion = models.CharField(max_length=50)
    
    descripcion = models.TextField()

    def _str_(self):
        return f'{self.operacion} en evento {self.evento_id}'  
    
class CotizacionDomicilio(models.Model):
    peso = models.FloatField(help_text="Peso en kilogramos del paquete.")
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def calcular_monto(self):
        """
        Método que calcula el monto aproximado a pagar según el peso.
        Suponiendo que:
        - Los primeros 5 kg cuestan $50 por kg.
        - Cada kg adicional cuesta $30.
        """
        if self.peso <= 5:
            self.monto = self.peso * 50  # $50 por kg para los primeros 5 kg
        else:
            self.monto = (5 * 50) + ((self.peso - 5) * 30)  # $30 por cada kg adicional

        self.save()  # Guardamos el monto calculado en la base de datos
        return self.monto
    
    def _str_(self):
        return f'Cotización: {self.peso} kg - ${self.monto}'
from decimal import Decimal
from django.conf import settings
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


    
    
class Usuario(AbstractUser):

    username = None  # Eliminamos el campo username predeterminado
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Usamos el email como identificador único
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    identificacion=models.TextField(max_length=10)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    USERNAME_FIELD = 'email'  # Especificamos que el email será el identificador principal
    REQUIRED_FIELDS = []  # Eliminamos username de los campos requeridos
    
    def __str__(self):
        return self.email




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
# modelos.py
from django.db import models

class CategoriaResiduo(models.Model):
    nombre = models.CharField(max_length=100)
    factor_co2 = models.FloatField(help_text="kg CO₂e evitado por kg de residuo")

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    
    categorias = models.ManyToManyField(CategoriaResiduo, through='UbicacionCategoria')

    def __str__(self):
        return self.nombre

class UbicacionCategoria(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaResiduo, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):                                                                                                                           
        return f"{self.ubicacion.nombre} - {self.categoria.nombre} (${self.precio})"

class RegistroResiduo(models.Model):
    categoria = models.ForeignKey(CategoriaResiduo, on_delete=models.CASCADE)
    cantidad_kg = models.FloatField()
    fecha = models.DateField(auto_now_add=True)

    @property
    def co2_evitable(self):
        return round(self.cantidad_kg * self.categoria.factor_co2, 2)  # Devuelve el CO₂ evitado

    def __str__(self):
        return f"{self.categoria.nombre} - {self.cantidad_kg} kg"
    
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ubicacion_categoria = models.ForeignKey(UbicacionCategoria, on_delete=models.CASCADE) 
    categoria = models.ForeignKey(CategoriaResiduo, on_delete=models.CASCADE)
    cantidad_kg = models.FloatField()
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username} - {self.categoria.nombre} en {self.ubicacion_categoria.ubicacion.nombre}"

    @property
    def precio_unitario(self):
        return self.ubicacion_categoria.precio

@property
def precio_total(self):
    return self.precio_unitario * Decimal(str(self.cantidad_kg))

class Factura(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura #{self.id} - {self.usuario.username} - {self.fecha.date()}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    categoria = models.ForeignKey('CategoriaResiduo', on_delete=models.CASCADE)
    cantidad_kg = models.FloatField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.categoria.nombre} - {self.cantidad_kg} kg"
    
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    #usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

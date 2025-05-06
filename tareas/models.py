from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
# Modelo para Profesores
from django.contrib.auth.models import AbstractUser
from django.db import models
from urllib.parse import quote
import requests
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UsuarioManager

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


    
    
class Usuario(AbstractUser):
    username = None  # Eliminamos el campo username predeterminado
    nombre = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    identificacion = models.CharField(max_length=10)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    # Atributos de clase (¡fuera de los campos!)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']  # Puedes dejar vacío si no necesitas campos obligatorios extra

    objects = UsuarioManager()
        
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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ubicaciones')

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
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Quien cotiza
    creador_ubicacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cotizaciones_recibidas')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('en_recoleccion', 'En Recolección'), ('recolectado', 'Recolectado')],
        default='pendiente'
    )

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

class Recoleccion(models.Model):
    factura = models.OneToOneField(
        Factura, 
        on_delete=models.CASCADE, 
        related_name='recoleccion',
        verbose_name="Factura asociada"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección",
        help_text="Calle y número, ej: Calle 100 #15-20"
    )
    ciudad = models.CharField(
        max_length=100,
        verbose_name="Ciudad/Municipio",
        help_text="Ciudad o municipio de recolección"
    )
    barrio = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Barrio/Localidad",
        help_text="Barrio o localidad (opcional)"
    )
    referencia = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Punto de referencia",
        help_text="Cerca a... o entre... (opcional)"
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones adicionales"
    )
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de solicitud"
    )

    class Meta:
        verbose_name = "Recolección"
        verbose_name_plural = "Recolecciones"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Recolección #{self.factura_id} - {self.direccion_completa()}"

    def direccion_completa(self):
        """Devuelve la dirección completa formateada"""
        partes = [
            self.direccion,
            self.barrio,
            self.ciudad,
            self.referencia
        ]
        return ", ".join(filter(None, partes))

    def geocodificar(self):
        """
        Obtiene las coordenadas (lat, lng) usando Nominatim
        Devuelve (latitud, longitud) o (None, None) si falla
        """
        direccion = quote(self.direccion_completa())
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={direccion}"
        
        try:
            response = requests.get(url, headers={
                'User-Agent': settings.APP_NAME  # Requerido por Nominatim
            })
            data = response.json()
            
            if data and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
        except Exception as e:
            print(f"Error en geocodificación: {e}")
        
        return None, None

    def obtener_mapa_embed_url(self, zoom=15):
        """
        Genera URL para iframe de OpenStreetMap
        Ejemplo de uso en templates:
        <iframe src="{{ recoleccion.obtener_mapa_embed_url }}" width="600" height="450"></iframe>
        """
        lat, lng = self.geocodificar()
        if lat and lng:
            return f"https://www.openstreetmap.org/export/embed.html?bbox={lng-0.01}%2C{lat-0.01}%2C{lng+0.01}%2C{lat+0.01}&layer=mapnik&marker={lat}%2C{lng}"
        return None

    @property
    def coordenadas(self):
        """Propiedad para acceder fácilmente a las coordenadas"""
        return self.geocodificar()

    def save(self, *args, **kwargs):
        # Aquí podrías agregar lógica para geocodificar automáticamente al guardar
        # si quisieras almacenar las coordenadas en la base de datos
        super().save(*args, **kwargs)
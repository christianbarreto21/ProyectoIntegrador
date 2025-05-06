from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CotizacionDomicilio, Empresa, Evento, Recoleccion, Rol, Usuario
from django.contrib.auth.forms import AuthenticationForm
from .models import Ubicacion

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'departamento', 'ciudad', 'direccion', 'fecha', 'hora']
 

class RegistroUsuarioForm(UserCreationForm):
    usable_password = None
    nombre = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=20, required=False)
    identificacion = forms.CharField(max_length=10, required=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'direccion', 'identificacion', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol, _ = Rol.objects.get_or_create(nombre="clientenatural")  # Asigna el rol automáticamente
        if commit:
            user.save()
        return user

from .models import Ubicacion, UbicacionCategoria, CategoriaResiduo
from django.forms import inlineformset_factory

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre', 'descripcion', 'latitud', 'longitud']
class RecoleccionForm(forms.ModelForm):
    class Meta:
        model = Recoleccion
        exclude = ['factura', 'fecha_solicitud']  # Se asignan automáticamente
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Calle 100 #15-20'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad o municipio'
            }),
            'barrio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cerca a..., entre... (opcional)'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 3
            }),
        }
        labels = {
            'direccion': 'Dirección',
            'ciudad': 'Ciudad/Municipio',
            'barrio': 'Barrio/Localidad',
            'referencia': 'Punto de referencia',
            'observaciones': 'Observaciones adicionales',
        }
        help_texts = {
            'direccion': 'Calle y número, ej: Calle 100 #15-20',
            'ciudad': 'Ciudad o municipio donde se realizará la recolección',
        }
class UbicacionCategoriaForm(forms.ModelForm):
    class Meta:
        model = UbicacionCategoria
        fields = ['categoria', 'precio']

UbicacionCategoriaFormSet = inlineformset_factory(
    Ubicacion,
    UbicacionCategoria,
    form=UbicacionCategoriaForm,
    extra=1,
    can_delete=True
)

class BuscarCategoriaForm(forms.Form):
    categoria = forms.CharField(max_length=100, label='Categoría', required=False)

class CotizacionDomicilioForm(forms.ModelForm):
    class Meta:
        model = CotizacionDomicilio
        fields = ['peso']
        widgets = {
            'peso': forms.NumberInput(attrs={'step': 'any', 'min': 0}),
        }
        
class InformeManejoResiduosForm(forms.Form):
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción del Manejo de Residuos")
    archivo_informe = forms.FileField(label="Archivo de Informe", required=False)

class InformeNormativasForm(forms.Form):
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción de la Normativa")
    archivo_informe = forms.FileField(label="Archivo de Informe", required=False)

from django import forms
from .models import CategoriaResiduo

class CategoriaResiduoForm(forms.ModelForm):
    class Meta:
        model = CategoriaResiduo
        fields = ['nombre', 'factor_co2'] 

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'latitud','longitud']

class BuscarCategoriaForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=CategoriaResiduo.objects.all(),
        label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
class RegistroGestorForm(UserCreationForm):
    usable_password = None
    class Meta:
        
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'direccion', 'identificacion', 'password1', 'password2']
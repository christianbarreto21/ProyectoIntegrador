from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CotizacionDomicilio, Evento, Rol, Usuario
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
    nombre = forms.CharField(max_length=150, required=True)
    identificacion = forms.CharField(max_length=20, required=True)
    correo = forms.EmailField(required=True)
    id_rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)

    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'identificacion', 'correo', 'id_rol', 'telefono', 'direccion', 'password1', 'password2']


from django import forms
from .models import Usuario, UsuarioResiduos

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'direccion']

class UsuarioResiduosForm(forms.ModelForm):
    class Meta:
        model = UsuarioResiduos
        fields = ['nombre', 'identificacion', 'correo', 'rol']


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre', 'descripcion', 'latitud', 'longitud', 'categoria']

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
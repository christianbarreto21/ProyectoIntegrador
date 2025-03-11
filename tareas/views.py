from datetime import timezone
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from django.contrib.auth import logout
import stripe
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from .models import Ubicacion
from django.shortcuts import render
from .models import Ubicacion, Usuario
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from .forms import CotizacionDomicilioForm, EventoForm, InformeManejoResiduosForm, InformeNormativasForm,  RegistroUsuarioForm, UsuarioForm, UsuarioResiduosForm
from django.contrib.auth import authenticate, login
from .forms import UbicacionForm
from django.core.files.storage import FileSystemStorage

def home1(request):
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect(reverse('login'))  # Redirige a la página de login

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Usuario

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige a la vista específica según el rol
                if user.usuario_residuos.rol.nombre == 'gestor de residuos':
                    return redirect('vista_gestor_residuos')
                elif user.usuario_residuos.rol.nombre == 'experto_ambiental':
                    return redirect('vista_experto_ambiental')
                elif user.usuario_residuos.rol.nombre == 'clienteempresa':
                    return redirect('vista_clienteempresa')
                elif user.usuario_residuos.rol.nombre == 'clientenatural':
                    return redirect('vista_clientenatural')
                else:
                    return redirect('home')  # Redirige a home si no hay coincidencia
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def vista_gestor_residuos(request):
    return render(request, 'gestor_residuos/gestor_residuos.html')

@login_required
def vista_experto_ambiental(request):
    return render(request, 'experto_ambiental.html')

@login_required
def vista_clienteempresa(request):
    return render(request, 'cliente_empresa/cliente_empresa.html')

@login_required
def vista_clientenatural(request):
    return render(request, 'cliente_natural/cliente_natural.html')

def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')

    

def cliente_empresa_dashboard(request):
    return render(request, 'cliente_empresa/cliente_empresa.html')

def cliente_natural(request):
    return render(request, 'cliente_natural/cliente_natural.html')

def gestor_dashboard(request):

    return render(request, 'gestor_dashboard.html')


#mapa

from django.core.serializers import serialize
from django.shortcuts import render
from .models import Ubicacion

def mapa_ubicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    ubicaciones_json = serialize('json', ubicaciones)
    return render(request, 'mapa_ubicaciones.html', {'ubicaciones_json': ubicaciones_json})


#pago
stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_view(request):
    return render(request, 'payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Crear una sesión de pago de Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Nombre del producto',
                            },
                            'unit_amount': 2000,  # Precio en centavos, ejemplo: $20.00
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.email = form.cleaned_data.get('correo')  # Establece el campo email desde correo
            usuario.save()
            login(request, usuario)
            return redirect('home')  # Cambia 'home' por la URL a la que quieras redirigir
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

# Crear un nuevo evento
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

# Listar todos los eventos
def listar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})

# Editar un evento
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {'form': form})

# Eliminar un evento
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        return redirect('listar_eventos')   
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})

@login_required
def ver_perfil(request):
    usuario = get_object_or_404(Usuario, username=request.user.username)
    return render(request, 'ver_perfil.html', {'usuario': usuario})

@login_required
def editar_perfil(request):
    usuario = get_object_or_404(Usuario, username=request.user.username)
    usuario_residuos = usuario.usuario_residuos

    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=usuario)
        residuos_form = UsuarioResiduosForm(request.POST, instance=usuario_residuos)
        
        if user_form.is_valid() and residuos_form.is_valid():
            user_form.save()
            residuos_form.save()
            return redirect('ver_perfil')  # Redirige a la vista de perfil
    else:
        user_form = UsuarioForm(instance=usuario)
        residuos_form = UsuarioResiduosForm(instance=usuario_residuos)

    return render(request, 'editar_perfil.html', {
        'user_form': user_form,
        'residuos_form': residuos_form
    })


def crear_ubicacion(request):
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mapa_ubicaciones')  # Redirige al mapa después de crear la ubicación
    else:
        form = UbicacionForm()
    return render(request, 'crear_ubicacion.html', {'form': form})
#filtro categorias
def ubicacion_list(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'ubicaciones/ubicacion_list.html', {'ubicaciones': ubicaciones})

def ubicacion_list1(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'ubicaciones/ubicacion_list1.html', {'ubicaciones': ubicaciones})
from .forms import BuscarCategoriaForm
def ubicacion_update(request, pk):
    ubicacion = get_object_or_404(Ubicacion, pk=pk)
    if request.method == 'POST':
        form = UbicacionForm(request.POST, instance=ubicacion)
        if form.is_valid():
            form.save()
            return redirect('ubicacion_detail', pk=ubicacion.pk)
    else:
        form = UbicacionForm(instance=ubicacion)
    return render(request, 'ubicaciones/ubicacion_form.html', {'form': form})

# Vista para eliminar una ubicación
def ubicacion_delete(request, pk):
    ubicacion = get_object_or_404(Ubicacion, pk=pk)
    if request.method == 'POST':
        ubicacion.delete()
        return redirect('ubicacion_list')  # Redirige a la lista de ubicaciones
    return render(request, 'ubicaciones/ubicacion_confirm_delete.html', {'ubicacion': ubicacion})


def buscar_por_categoria(request):
    ubicaciones = None
    form = BuscarCategoriaForm(request.GET)
    
    if form.is_valid():
        categoria = form.cleaned_data.get('categoria')
        if categoria:
            ubicaciones = Ubicacion.objects.filter(categoria__icontains=categoria)  # Filtra por categoría

    return render(request, 'ubicaciones/buscar.html', {'form': form, 'ubicaciones': ubicaciones})

def cotizar_domicilio(request):
    monto = None
    form = CotizacionDomicilioForm(request.POST or None)
    
    if form.is_valid():
        cotizacion = form.save(commit=False)
        cotizacion.calcular_monto()  # Calcula el monto según el peso
        monto = cotizacion.monto  # Guardamos el monto calculado

    return render(request, 'cotizaciones/cotizar_domicilio.html', {'form': form, 'monto': monto})
#expe
@login_required
def agregar_informe_manejo_residuos(request):
    """
    Vista para agregar un informe de manejo de residuos.
    """
    if request.method == 'POST':
        form = InformeManejoResiduosForm(request.POST, request.FILES)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            archivo = form.cleaned_data['archivo_informe']
            
            # Guardar archivo en el sistema de archivos
            if archivo:
                fs = FileSystemStorage()
                filename = fs.save(archivo.name, archivo)
                file_url = fs.url(filename)
            
            # Confirmación de éxito
            return render(request, 'informes/informe_exitoso.html', {
                'descripcion': descripcion,
                'file_url': file_url,
            })
    else:
        form = InformeManejoResiduosForm()

    return render(request, 'informes/agregar_informe.html', {'form': form, 'titulo': 'Informe de Manejo de Residuos'})


@login_required
def agregar_informe_normativas(request):
    """
    Vista para agregar un informe de normativas.
    """
    if request.method == 'POST':
        form = InformeNormativasForm(request.POST, request.FILES)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            archivo = form.cleaned_data['archivo_informe']
            
            # Guardar archivo en el sistema de archivos
            if archivo:
                fs = FileSystemStorage()
                filename = fs.save(archivo.name, archivo)
                file_url = fs.url(filename)
            
            # Confirmación de éxito
            return render(request, 'informes/informe_exitoso.html', {
                'descripcion': descripcion,
                'file_url': file_url,
            })
    else:
        form = InformeNormativasForm()

    return render(request, 'informes/agregar_informe.html', {'form': form, 'titulo': 'Informe de Normativas'})
from django.shortcuts import render, redirect
from .models import Auto, Lainaus
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from datetime import datetime

# Función para obtener los datos del formulario
def get_lainaus_form_data(request):
    return {
        'opiskelija_etunimi': request.POST.get('etunimi'),
        'opiskelija_sukunimi': request.POST.get('sukunimi'),
        'opiskelija_henkilotunnus': request.POST.get('henkilotunnus'),
        'opiskelija_id': request.POST.get('opiskelija_id'),
        'ajokorti_id': request.POST.get('ajokorti_id'),
        'lainaus_pvm': request.POST.get('lainaus_pvm'),
        'palautus_pvm': request.POST.get('palautus_pvm'),
    }

# Función para convertir cadenas de fecha en objetos datetime
def parse_datetime(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return None

# Función para obtener un auto por ID
def get_auto(auto_id):
    try:
        return Auto.objects.get(id=auto_id)
    except Auto.DoesNotExist:
        return None

# Función para generar el código de barras con el Ajokorti ID
def generate_barcode_with_id(ajokorti_id):
    try:
        code128 = barcode.get_barcode_class('code128')
        barcode_obj = code128(ajokorti_id, writer=ImageWriter())
        barcode_io = BytesIO()
        barcode_obj.write(barcode_io)
        barcode_io.seek(0)
        return barcode_io
    except Exception as e:
        print(f"Error al generar el código de barras: {e}")
        return None

# Función para crear un préstamo (Lainaus) en la base de datos
def create_lainaus(data, auto):
    try:
        return Lainaus.objects.create(
            opiskelija_etunimi=data['opiskelija_etunimi'],
            opiskelija_sukunimi=data['opiskelija_sukunimi'],
            opiskelija_henkilotunnus=data['opiskelija_henkilotunnus'],
            opiskelija_id=data['opiskelija_id'],
            ajokorti_id=data['ajokorti_id'],
            lainaus_pvm=data['lainaus_pvm'],
            palautus_pvm=data['palautus_pvm'],
            auto=auto
        )
    except Exception as e:
        print(f"Error al crear el préstamo: {e}")
        return None

# Vista de administración de autos
def hallinto_view(request):
    if request.method == "POST":
        # Validar datos del formulario
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        ano = request.POST.get('ano')
        kilometraje = request.POST.get('kilometraje')
        estado = request.POST.get('estado')

        # Crear un nuevo Auto
        try:
            Auto.objects.create(
                marca=marca,
                modelo=modelo,
                color=color,
                ano=ano,
                kilometraje=kilometraje,
                estado=estado
            )
        except Exception as e:
            return HttpResponse(f"Error al guardar el auto: {e}", status=400)

        return redirect('hallinto')

    # Obtener todos los autos
    autot = Auto.objects.all()
    return render(request, 'rasekoautolainaus/hallinto.html', {'autot': autot})

# Vista de préstamo de un automóvil
def lainaus_view(request, auto_id):
    if request.method == "POST":
        return process_lainaus_form(request, auto_id)

    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Auto no encontrado.", status=404)

    barcode_image = generate_barcode_with_id(auto_id)
    return render(request, 'rasekoautolainaus/lainaus.html', {'auto': auto, 'barcode_image': barcode_image})

# Procesar datos del formulario de préstamo
def process_lainaus_form(request, auto_id):
    form_data = get_lainaus_form_data(request)

    # Validar fechas
    lainaus_pvm = parse_datetime(form_data['lainaus_pvm'])
    palautus_pvm = parse_datetime(form_data['palautus_pvm'])
    if not lainaus_pvm or not palautus_pvm:
        return HttpResponse("Fecha inválida.", status=400)

    # Obtener el auto correspondiente
    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Auto no encontrado.", status=404)

    # Generar código de barras
    barcode_image = generate_barcode_with_id(form_data['ajokorti_id'])
    if barcode_image is None:
        return HttpResponse("Error al generar el código de barras.", status=400)

    # Crear el préstamo
    lainaus = create_lainaus(form_data, auto)
    if lainaus is None:
        return HttpResponse("Error al guardar el préstamo.", status=500)

    return redirect('hallinto')

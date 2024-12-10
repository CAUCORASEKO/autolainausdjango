from django.shortcuts import render, redirect
from .models import Auto, Lainaus
from django.http import HttpResponse
import barcode
import base64
from barcode.writer import ImageWriter
from io import BytesIO
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML

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
    if not ajokorti_id:
        print("El valor de ajokorti_id es inválido:", ajokorti_id)
        return None

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

# Vista para el préstamo de un automóvil (GET y POST)
def lainaus_view(request, auto_id):
    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Auto no encontrado.", status=404)

    barcode_image = None  # Inicializamos la imagen de código de barras

    if request.method == "POST":
        # Usar una named expression para simplificar la verificación de ajokorti_id
        if ajokorti_id := request.POST.get('ajokorti_id'):
            barcode_image = generate_barcode_with_id(ajokorti_id)
        
        # Guardamos el préstamo en la base de datos incluso si no se puede generar el código de barras
        return process_lainaus_form(request, auto_id, barcode_image)

    # Si es un GET, simplemente renderizamos el formulario
    return render(request, 'rasekoautolainaus/lainaus.html', {
        'auto': auto,
        'barcode_image': barcode_image
    })


# Procesar datos del formulario de préstamo y generar vista imprimible
def process_lainaus_form(request, auto_id, barcode_image=None):
    form_data = get_lainaus_form_data(request)

    lainaus_pvm = parse_datetime(form_data['lainaus_pvm'])
    palautus_pvm = parse_datetime(form_data['palautus_pvm'])
    if not lainaus_pvm or not palautus_pvm:
        return HttpResponse("Fecha inválida.", status=400)

    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Auto no encontrado.", status=404)

    # Intentar generar el código de barras si no se proporcionó
    barcode_image = barcode_image or generate_barcode_with_id(form_data['ajokorti_id'])
    if barcode_image is None:
        print("No se pudo generar el código de barras, pero el préstamo se guarda.")
    
    # Crear el préstamo en la base de datos
    lainaus = create_lainaus(form_data, auto)
    if lainaus is None:
        return HttpResponse("Error al guardar el préstamo.", status=500)

    # Si hay un código de barras, intentamos generar el archivo PDF
    if barcode_image:
        html_content = render_to_string('rasekoautolainaus/lainaus_imprimible.html', {
            'lainaus': lainaus,
            'auto': auto,
            'barcode_image': base64.b64encode(barcode_image.getvalue()).decode('utf-8'),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="lainaus_{lainaus.id}.pdf"'
        HTML(string=html_content).write_pdf(response)

        return response
    else:
        return HttpResponse(f"Préstamo {lainaus.id} guardado sin código de barras o PDF.", status=200)

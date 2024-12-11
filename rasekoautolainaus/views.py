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

# Funktio lomaketietojen hakemiseen
# Tämä funktio lukee tiedot HTTP POST -pyynnöstä ja palauttaa ne sanakirjana
# Lomaketiedot sisältävät lainauksen ja opiskelijan tiedot

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

# Funktio muuntaa merkkijonon datetime-objektiksi
# Käytätään validoimaan ja tulkitsemaan lomaketietoja

def parse_datetime(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return None

# Funktio hakee Auto-objektin ID:n perusteella
# Jos autoa ei löydy, palautetaan None

def get_auto(auto_id):
    try:
        return Auto.objects.get(id=auto_id)
    except Auto.DoesNotExist:
        return None

# Funktio viivakoodin generointiin ajokortti-ID:llä
# Tämä luo viivakoodin, joka sisältää annettavan ajokortti-ID:n

def generate_barcode_with_id(ajokorti_id):
    if not ajokorti_id:
        print("Ajokortti-ID ei ole kelvollinen:", ajokorti_id)
        return None

    try:
        code128 = barcode.get_barcode_class('code128')
        barcode_obj = code128(ajokorti_id, writer=ImageWriter())
        barcode_io = BytesIO()
        barcode_obj.write(barcode_io)
        barcode_io.seek(0)
        return barcode_io
    except Exception as e:
        print(f"Virhe viivakoodin generoinnissa: {e}")
        return None

# Funktio uuden lainauksen luomiseksi tietokantaan
# Luo Lainaus-objektin ja tallentaa sen

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
        print(f"Virhe lainauksen luomisessa: {e}")
        return None

# Hallintasivu autojen lisäämiseen ja hallintaan
# GET: palauttaa lista kaikista autoista
# POST: lisää uuden auton tietokantaan

def hallinto_view(request):
    if request.method == "POST":
        # Haetaan lomaketiedot
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        ano = request.POST.get('ano')
        kilometraje = request.POST.get('kilometraje')
        estado = request.POST.get('estado')

        # Yritetään luoda uusi Auto-objekti
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
            return HttpResponse(f"Virhe auton tallentamisessa: {e}", status=400)

        return redirect('hallinto')

    # Haetaan kaikki autot tietokannasta
    autot = Auto.objects.all()
    return render(request, 'rasekoautolainaus/hallinto.html', {'autot': autot})

# Funktio auton lainaamiseen (GET ja POST)
def lainaus_view(request, auto_id):
    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Autoa ei löydy.", status=404)

    barcode_image = None  # Alustetaan viivakoodikuva

    if request.method == "POST":
        # Haetaan ajokortti-ID ja luodaan viivakoodi
        if ajokorti_id := request.POST.get('ajokorti_id'):
            barcode_image = generate_barcode_with_id(ajokorti_id)

        # Käsitellään lainauslomake ja palataan tulos
        return process_lainaus_form(request, auto_id, barcode_image)

    # Jos on GET, palautetaan lomake
    return render(request, 'rasekoautolainaus/lainaus.html', {
        'auto': auto,
        'barcode_image': barcode_image
    })

# Käsittele lainauslomake ja luo näkymä tulostamista varten
def process_lainaus_form(request, auto_id, barcode_image=None):
    form_data = get_lainaus_form_data(request)

    lainaus_pvm = parse_datetime(form_data['lainaus_pvm'])
    palautus_pvm = parse_datetime(form_data['palautus_pvm'])
    if not lainaus_pvm or not palautus_pvm:
        return HttpResponse("Päiväys ei ole kelvollinen.", status=400)

    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Autoa ei löydy.", status=404)

    # Yritetään luoda viivakoodi, jos sitä ei ole jo annettu
    barcode_image = barcode_image or generate_barcode_with_id(form_data['ajokorti_id'])
    if barcode_image is None:
        print("Viivakoodia ei voitu luoda, mutta lainaus tallennetaan.")

    # Luodaan lainaus tietokantaan
    lainaus = create_lainaus(form_data, auto)
    if lainaus is None:
        return HttpResponse("Virhe lainauksen tallentamisessa.", status=500)

    # Jos viivakoodi on olemassa, luodaan PDF-tiedosto
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

    # Palautetaan onnistumisviesti ilman PDF-tiedostoa
    return HttpResponse(f"Lainaus {lainaus.id} tallennettu ilman viivakoodia tai PDF-tiedostoa.", status=200)


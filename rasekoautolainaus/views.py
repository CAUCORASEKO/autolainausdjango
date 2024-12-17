from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Auto, Lainaus
import barcode
import base64
from barcode.writer import ImageWriter
from io import BytesIO
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML

# --- Autentikointi ja käyttäjänhallinta ---

# Kirjautumissivu
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('hallinto')  # Siirry hallintasivulle
        return render(request, 'rasekoautolainaus/login.html', {'error_message': 'Käyttäjätunnus tai salasana on virheellinen.'})
    return render(request, 'rasekoautolainaus/login.html')

# Kirjautuminen ulos
def logout_view(request):
    logout(request)
    return redirect('login')


# --- Autohallinta ---

# Hallintasivu autojen lisäämiseen ja listaamiseen
@login_required
def hallinto_view(request):
    if request.method == "POST":
        # Tallenna uusi auto tietokantaan
        try:
            Auto.objects.create(
                marca=request.POST.get('marca'),
                modelo=request.POST.get('modelo'),
                color=request.POST.get('color'),
                ano=request.POST.get('ano'),
                kilometraje=request.POST.get('kilometraje'),
                estado=request.POST.get('estado')
            )
        except Exception as e:
            return HttpResponse(f"Virhe auton tallentamisessa: {e}", status=400)
        return redirect('hallinto')

    # Listaa kaikki autot
    autot = Auto.objects.all()
    return render(request, 'rasekoautolainaus/hallinto.html', {'autot': autot})


# --- Lainaushallinta ---

# Näytä lainauslomake tai käsittele auton lainausta
def lainaus_view(request, auto_id):
    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Autoa ei löydy.", status=404)

    barcode_image = None

    if request.method == "POST":
        # Luo lainaus ja viivakoodi
        if ajokorti_id := request.POST.get('ajokorti_id'):
            barcode_image = generate_barcode_with_id(ajokorti_id)
        return process_lainaus_form(request, auto_id, barcode_image)

    return render(request, 'rasekoautolainaus/lainaus.html', {'auto': auto, 'barcode_image': barcode_image})


# Palauta auto ja merkitse lainaus palautetuksi
def palautus_view(request, lainaus_id):
    lainaus = get_object_or_404(Lainaus, id=lainaus_id)

    if request.method == "POST":
        lainaus.palautus_pvm = datetime.now()
        lainaus.save()

        auto = lainaus.auto
        auto.estado = 'Palautettu'
        auto.save()
        return HttpResponse(f"Auto palautettu, lainaus ID: {lainaus.id} on nyt palautettu.", status=200)

    return render(request, 'rasekoautolainaus/palautus.html', {'lainaus': lainaus})


# --- Viivakoodi ja PDF-hallinta ---

# Luo ja käsittele lainauksen lomake
def process_lainaus_form(request, auto_id, barcode_image=None):
    form_data = get_lainaus_form_data(request)
    lainaus_pvm = parse_datetime(form_data['lainaus_pvm'])
    palautus_pvm = parse_datetime(form_data['palautus_pvm'])

    if not lainaus_pvm or not palautus_pvm:
        return HttpResponse("Päiväys ei ole kelvollinen.", status=400)

    auto = get_auto(auto_id)
    if not auto:
        return HttpResponse("Autoa ei löydy.", status=404)

    barcode_image = barcode_image or generate_barcode_with_id(form_data['ajokorti_id'])
    lainaus = create_lainaus(form_data, auto)

    if lainaus is None:
        return HttpResponse("Virhe lainauksen tallentamisessa.", status=500)

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

    return HttpResponse(f"Lainaus {lainaus.id} tallennettu ilman viivakoodia tai PDF-tiedostoa.", status=200)


# Generoi viivakoodi ajokortti-ID:lle
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


# --- Apufunktiot ---

# Hae lainauksen lomaketiedot
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


# Hae Auto-objekti ID:llä
def get_auto(auto_id):
    try:
        return Auto.objects.get(id=auto_id)
    except Auto.DoesNotExist:
        return None


# Muunna päivämäärä merkkijonosta datetime-objektiksi
def parse_datetime(date_str):
    try:
        if 'T' in date_str:
            date_str = date_str.replace('T', ' ')
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return None


# Luo uusi lainaus tietokantaan
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

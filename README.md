# AutolainausDjango

AutolainausDjango on ajoneuvojen lainausjärjestelmä, joka on rakennettu Django-kehystä käyttäen. Järjestelmä mahdollistaa ajoneuvojen rekisteröinnin, lainojen hallinnan ja varausten seurannan tehokkaasti.

## Teknologiat
- **Django**: Web-kehys backendille.
- **SQLite**: Oletustietokanta (myöhemmin siirretty PostgreSQL:ään).
- **Python 3.11**: Ohjelmointikieli.
- **Bootstrap**: Käytetty käyttöliittymän suunnitteluun (löytyy kansiosta `static/css`).
- Muut riippuvuudet on listattu tiedostossa `requirements.txt`.

## Asennusohjeet
Seuraa näitä vaiheita asentaaksesi projektin paikallisesti:

1. Kloonaa repositorio:

```bash
   git clone https://github.com/CAUCORASEKO/taskplanner-CAUCORASEKO.git   
```

Siirry projektikansioon:

```bash
cd taskplanner-CAUCORASEKO
```

Luo ja aktivoi virtuaaliympäristö:
macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```
Asenna riippuvuudet:
```bash
pip install -r requirements.txt
```
(Valinnainen) Jos käytät PostgreSQL:ää, määritä tietokannan asetukset .env-tiedostossa (esim. DATABASE_URL). Jos käytät SQLiteä, tätä vaihetta ei tarvita.

Suorita tietokantamigraatiot:
```bash
python manage.py migrate
```

Luo pääkäyttäjä (superuser) hallintapaneelia varten:
```bash
python manage.py createsuperuser
```

Käynnistä kehityspalvelin:

```bash
python manage.py runserver
```

Avaa selaimessa: http://127.0.0.1:8000/.

Käyttöohjeet
Järjestelmään pääsy: Kun palvelin on käynnissä, voit käyttää järjestelmää osoitteessa http://127.0.0.1:8000/.

Hallintapaneeli: Kirjaudu sisään pääkäyttäjällä osoitteessa http://127.0.0.1:8000/admin/. Täältä voit hallita ajoneuvoja ja lainoja.

Käyttöliittymä: Käyttöliittymä on suunniteltu Bootstrapilla, ja sen tiedostot sijaitsevat kansiossa frontend/taskplanner-frontend/node_modules. Varmista, että tyylit ja skriptit on linkitetty oikein.

Tuotantoon vienti
Ohjeet projektin julkaisemiseen tuotantoympäristöön (esimerkiksi Render-palveluun):
Luo tili Renderiin ja yhdistä GitHub-repositoriosi (taskplanner-CAUCORASEKO).

Määritä ympäristömuuttujat Renderissä:
SECRET_KEY: Djangon salainen avain.

DATABASE_URL: Tietokannan URL (esim. PostgreSQL).

DEBUG: Aseta arvoksi False tuotannossa.

Käytä requirements.txt-tiedostoa riippuvuuksien asentamiseen.

Määritä käynnistysskripti, joka suorittaa migraatiot ja käynnistää palvelimen:

```bash
python manage.py migrate
```
gunicorn autolainausdjango.wsgi:application

Varmista, että staattiset tiedostot (static/) on konfiguroitu oikein tuotantoa varten (voit käyttää komentoa python manage.py collectstatic).

## Versionhallinta ja yhteistyösäännöt

## Haarat:

Käytä main-haaraa päähaarana.

Luo uusia haaroja ominaisuuksille tai korjauksille, esimerkiksi feature/uusi-ominaisuus tai bugfix/korjaa-virhe.

## Pull requestit:

Kaikki muutokset tulee tehdä pull requestien kautta.

Vähintään yhden tiimin jäsenen tulee tarkastaa ja hyväksyä pull request ennen sen yhdistämistä main-haaraan.

## Lisätiedot ja yhteystiedot

Tiimin jäsen: Claudio Valenzuela (claudio.fernando.valenzuela@gmail.com).

## Huomautus:

Tämä projekti kehitettiin alun perin repositoriossa autolainausdjango ja integroitiin myöhemmin taskplanner-CAUCORASEKO-repositorioon kurssin vaatimusten täyttämiseksi.


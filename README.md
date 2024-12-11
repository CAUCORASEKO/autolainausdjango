# Ajoneuvon lainausjärjestelmä

Tämä projekti on ajoneuvon lainausjärjestelmä, joka on rakennettu Django-kehyksellä.

## Asennus

1. Klonaa tämä repositorio paikallisesti:
   ```bash
   git clone https://github.com/CAUCORASEKO/autolainausdjango.git


## Siirry projektikansioon:
```
cd autolainausdjango

```
## Luo ja aktivoi virtuaaliympäristö:

```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

```
## Asenna tarvittavat riippuvuudet:

```
pip install -r requirements.txt

```
## Suorita migraatiot:

```
python manage.py migrate

```
Käynnistä kehityspalvelin:

```
python manage.py runserver

```
## Avaa selaimessa: http://127.0.0.1:8000/


from django.db import models

class Auto(models.Model):
    marca = models.CharField(max_length=100)  # Auton merkki
    modelo = models.CharField(max_length=100)  # Auton malli
    color = models.CharField(max_length=50)  # Auton väri
    ano = models.PositiveIntegerField()  # Valmistusvuosi
    kilometraje = models.PositiveIntegerField()  # Ajokilometrit
    estado = models.TextField(blank=True, null=True)  # Lisähuomiot autosta

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.color})"

class Lainaus(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="lainaukset")  # Viite lainattavaan autoon
    opiskelija_etunimi = models.CharField(max_length=100)  # Opiskelijan etunimi
    opiskelija_sukunimi = models.CharField(max_length=100)  # Opiskelijan sukunimi
    opiskelija_henkilotunnus = models.CharField(max_length=11)  # Opiskelijan henkilötunnus
    opiskelija_id = models.CharField(max_length=20)  # Opiskelijan tunniste
    ajokorti_id = models.CharField(max_length=20)  # Ajokortin tunniste
    lainaus_pvm = models.DateTimeField()  # Lainauksen aloituspäivä ja aika
    palautus_pvm = models.DateTimeField()  # Lainauksen palautuspäivä ja aika
    
    
    
class Lainaus(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="lainaukset")  # Viite lainattavaan autoon
    opiskelija_etunimi = models.CharField(max_length=100)  # Opiskelijan etunimi
    opiskelija_sukunimi = models.CharField(max_length=100)  # Opiskelijan sukunimi
    opiskelija_henkilotunnus = models.CharField(max_length=11)  # Opiskelijan henkilötunnus
    opiskelija_id = models.CharField(max_length=20)  # Opiskelijan tunniste
    ajokorti_id = models.CharField(max_length=20)  # Ajokortin tunniste
    lainaus_pvm = models.DateTimeField()  # Lainauksen aloituspäivä ja aika
    palautus_pvm = models.DateTimeField(null=True, blank=True)  # Lainauksen palautuspäivämäärä ja aika
    palautettu = models.BooleanField(default=False)  # Campo que indica si el auto ha sido devuelto

    def __str__(self):
        return f"{self.opiskelija_etunimi} {self.opiskelija_sukunimi} - {self.auto}"


    def __str__(self):
        return f"{self.opiskelija_etunimi} {self.opiskelija_sukunimi} - {self.auto}"

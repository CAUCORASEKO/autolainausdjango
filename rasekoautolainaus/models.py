from django.db import models

class Auto(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    ano = models.PositiveIntegerField()
    kilometraje = models.PositiveIntegerField()
    estado = models.TextField(blank=True, null=True)  # Campo para notas del auto

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.color})"

class Lainaus(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="lainaukset")
    opiskelija_etunimi = models.CharField(max_length=100)
    opiskelija_sukunimi = models.CharField(max_length=100)
    opiskelija_henkilotunnus = models.CharField(max_length=11)
    opiskelija_id = models.CharField(max_length=20)
    ajokorti_id = models.CharField(max_length=20)
    lainaus_pvm = models.DateTimeField()
    palautus_pvm = models.DateTimeField()

    def __str__(self):
        return f"{self.opiskelija_etunimi} {self.opiskelija_sukunimi} - {self.auto}"

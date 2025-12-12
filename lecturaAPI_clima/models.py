from django.db import models

class WeatherSearch(models.Model):
    localidad = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()
    temp_max = models.FloatField()
    temp_min = models.FloatField()
    lluvia = models.FloatField()
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.localidad
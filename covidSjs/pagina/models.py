from django.db import models

# Create your models here.

class casos (models.Model):
    data = models.DateField(primary_key=True)
    confirmados = models.IntegerField()
    recuperados = models.IntegerField()
    suspeitos = models.IntegerField()
    descartados = models.IntegerField()
    obitos = models.IntegerField()

    class Meta:
        verbose_name_plural = 'casos'
        get_latest_by = 'data'

    def __str__(self):
        #converte do formato ano-mes-dia para dia/mes/ano e transforma em string
        return self.data.strftime('%d/%m/%Y')
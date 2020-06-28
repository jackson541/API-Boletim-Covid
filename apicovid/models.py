from django.db import models

class Caso(models.Model):
    TIPO_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('tratamento', 'Em tratamento'),
        ('internado', 'Internado'),
        ('recuperado', 'Recuperado'),
        ('suspeito', 'Suspeito'),
        ('obito', 'Óbito'),
        ('descartado', 'Descartado'),
        ('notificado', 'Notificado')
    ]

    GENERO_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
        ('outro', 'Outro')
    ]

    FAIXA_CHOICES = [
        ('0-20', '0-20'),
        ('20-40', '20-40'),
        ('40-60', '40-60'),
        ('60-70', '60-70'),
        ('70-80', '70-80'),
        ('80+', '80+')
    ]

    # alterar para ForeignKey quando o model de boletim for criado
    boletim = models.IntegerField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='notificado')
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default='feminino')
    faixa = models.CharField(max_length=5, choices=FAIXA_CHOICES, default='0-20')
    

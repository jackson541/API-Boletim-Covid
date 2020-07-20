# Arquivo para armazenar todas as choices utilizadas no models.py

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
    ('0-19', '0-19'),
    ('20-39', '20-39'),
    ('40-59', '40-59'),
    ('60-69', '60-69'),
    ('70-79', '70-79'),
    ('80+', '80+')
]

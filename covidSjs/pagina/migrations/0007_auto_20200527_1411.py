# Generated by Django 3.0.6 on 2020-05-27 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0006_delete_teste'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casos',
            options={'get_latest_by': 'data', 'verbose_name_plural': 'casos'},
        ),
    ]

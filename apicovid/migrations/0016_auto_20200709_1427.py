# Generated by Django 3.0.7 on 2020-07-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicovid', '0015_auto_20200709_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boletim',
            name='data',
            field=models.DateTimeField(),
        ),
    ]

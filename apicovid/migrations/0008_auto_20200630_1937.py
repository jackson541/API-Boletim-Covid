# Generated by Django 3.0.7 on 2020-06-30 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apicovid', '0007_merge_20200630_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apicovid.Cidade'),
        ),
    ]

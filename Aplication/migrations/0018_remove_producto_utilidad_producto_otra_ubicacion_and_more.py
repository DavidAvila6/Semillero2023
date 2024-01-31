# Generated by Django 4.2.7 on 2024-01-31 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplication', '0017_alter_producto_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='utilidad',
        ),
        migrations.AddField(
            model_name='producto',
            name='otra_ubicacion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='modelo',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='producto',
            name='ubicacion',
            field=models.CharField(choices=[('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'), ('A6', 'A6'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'), ('B6', 'B6'), ('C3', 'C3'), ('C4', 'C4'), ('C5', 'C5'), ('C6', 'C6'), ('C7', 'C7'), ('C8', 'C8'), ('T1', 'T1'), ('T2', 'T2'), ('OTRO', 'Otro')], default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='carnet',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='carrera',
            field=models.CharField(choices=[('IngAmbiental', 'Ingeniería Ambiental'), ('IngIndustrial', 'Ingeniería Industrial'), ('CompIA', 'Ciencias de la Computación e IA'), ('IngElectronica', 'Ingeniería Electrónica'), ('Matematicas', 'Matemáticas')], max_length=100),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo_electronico',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]

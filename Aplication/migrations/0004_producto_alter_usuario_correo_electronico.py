# Generated by Django 4.2.4 on 2023-10-24 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplication', '0003_usuario_correo_electronico_alter_usuario_carnet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('marca', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo_electronico',
            field=models.EmailField(max_length=255),
        ),
    ]

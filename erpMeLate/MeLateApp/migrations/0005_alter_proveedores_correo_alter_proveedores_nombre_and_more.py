# Generated by Django 4.2.1 on 2023-05-20 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "MeLateApp",
            "0004_alter_proveedores_correo_alter_proveedores_nombre_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="proveedores",
            name="correo",
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name="proveedores",
            name="nombre",
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name="proveedores", name="telefono", field=models.BigIntegerField(),
        ),
    ]
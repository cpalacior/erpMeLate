# Generated by Django 4.2.1 on 2023-05-22 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("MeLateApp", "0007_remove_insumos_categoria_insumos_proveedor"),
    ]

    operations = [
        migrations.RenameField(
            model_name="admin", old_name="nombre", new_name="usuario",
        ),
    ]

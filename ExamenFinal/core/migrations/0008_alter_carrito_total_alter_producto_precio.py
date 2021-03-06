# Generated by Django 4.0.1 on 2022-07-08 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_carrito_total_alter_producto_categoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

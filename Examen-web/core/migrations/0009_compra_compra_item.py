# Generated by Django 4.0.4 on 2022-07-10 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_alter_carrito_total_alter_producto_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de compra')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(max_length=200, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Compra_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_compra', to='core.compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
        ),
    ]
# Generated by Django 4.1 on 2022-08-08 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("appBIOEAFIT", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "identificacion",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("nombre", models.CharField(max_length=45)),
                ("correo", models.CharField(max_length=45)),
                ("clave", models.CharField(max_length=30)),
                ("dieccion", models.CharField(max_length=50)),
                ("edad", models.SmallIntegerField()),
                ("telefono", models.BigIntegerField()),
                (
                    "idtipousuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appBIOEAFIT.tipousuario",
                    ),
                ),
            ],
        ),
    ]

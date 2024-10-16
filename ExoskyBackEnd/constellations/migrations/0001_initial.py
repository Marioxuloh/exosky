# Generated by Django 5.1.1 on 2024-10-05 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exoplanets', '0002_alter_exoplanet_pl_name'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordenates', models.JSONField()),
                ('exoplanet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exoplanets.exoplanet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]

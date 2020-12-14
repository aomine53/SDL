# Generated by Django 2.2 on 2020-12-14 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20201212_2101'),
        ('userforms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('device_parameters', models.TextField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile')),
            ],
        ),
    ]

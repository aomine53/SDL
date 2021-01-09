# Generated by Django 2.2 on 2021-01-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210104_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagAssign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=100)),
                ('tag_id', models.CharField(max_length=50)),
                ('station_pos', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]

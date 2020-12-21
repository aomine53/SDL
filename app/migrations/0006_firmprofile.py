# Generated by Django 2.2 on 2020-11-30 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_userprofile_email_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirmProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=300, null=True)),
                ('company_email', models.EmailField(max_length=254, null=True)),
                ('company_telephone', models.CharField(max_length=100, null=True)),
                ('company_address1', models.CharField(max_length=1000, null=True)),
                ('company_address2', models.CharField(max_length=1000, null=True)),
                ('company_country', models.CharField(max_length=100, null=True)),
                ('company_state', models.CharField(max_length=100, null=True)),
                ('company_city', models.CharField(max_length=100, null=True)),
                ('company_zip', models.CharField(max_length=100, null=True)),
                ('company_gstn', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
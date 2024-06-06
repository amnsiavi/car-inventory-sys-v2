# Generated by Django 5.0.6 on 2024-06-06 06:25

import App_Inventory.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('price', models.CharField(max_length=50)),
                ('mileage', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('is_avaliable', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=App_Inventory.models.upload_to)),
                ('QR_CODE', models.ImageField(upload_to='qrcodes')),
                ('created', models.DateTimeField(default='2024-06-06-06:25:19')),
                ('updated', models.DateTimeField(default='2024-06-06-06:25:19')),
            ],
        ),
    ]
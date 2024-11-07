# Generated by Django 5.1.2 on 2024-11-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('command_before', models.TextField(blank=True, null=True)),
                ('command_after', models.TextField(blank=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.GenericIPAddressField()),
                ('host_user', models.CharField(max_length=50)),
                ('host_password', models.CharField(blank=True, max_length=200, null=True)),
                ('host_dir', models.CharField(max_length=255)),
                ('host_cert', models.CharField(blank=True, max_length=255, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

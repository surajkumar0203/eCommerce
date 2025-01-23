# Generated by Django 5.1.4 on 2025-01-20 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('email_token', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='customer/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shopkeeper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('email_token', models.CharField(blank=True, max_length=100, null=True)),
                ('gst_number', models.CharField(max_length=15)),
                ('aadhar_number', models.CharField(max_length=14)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='shopkeeper/')),
                ('bmp_id', models.CharField(max_length=100, unique=True)),
                ('vender_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

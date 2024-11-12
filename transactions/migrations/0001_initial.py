# Generated by Django 5.1.3 on 2024-11-12 12:10

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED'), ('PENDING', 'PENDING')], max_length=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account_number', models.CharField(max_length=11)),
                ('transaction_type', models.CharField(default='DEPOSIT', max_length=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'DEPOSIT'), ('WITHDRAWAL', 'WITHDRAWAL'), ('TRANSFER', 'TRANSFER')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED'), ('PENDING', 'PENDING')], max_length=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('source_account_number', models.CharField(max_length=11)),
                ('destination_account_number', models.CharField(max_length=11)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED'), ('PENDING', 'PENDING')], max_length=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account_number', models.CharField(max_length=11)),
                ('transaction_type', models.CharField(default='WITHDRAWAL', max_length=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
    ]

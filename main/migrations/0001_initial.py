# Generated by Django 4.0.6 on 2022-07-21 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Holder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holder_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ItemTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='TechUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('Installed', 'Installed'), ('In hands of', 'In hands of'), ('Warehouse', 'Warehouse')], default='Warehouse', max_length=200, null=True)),
                ('registration_key', models.CharField(blank=True, max_length=200, null=True)),
                ('home_id', models.CharField(blank=True, max_length=200, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.techuser')),
                ('held_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.holder')),
                ('item_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.itemtype')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.itemtitle')),
            ],
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation_date', models.DateTimeField(auto_now_add=True)),
                ('reg_key', models.CharField(blank=True, max_length=200, null=True)),
                ('installed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.holder')),
                ('items_used', models.ManyToManyField(to='main.inventoryitem')),
            ],
        ),
    ]

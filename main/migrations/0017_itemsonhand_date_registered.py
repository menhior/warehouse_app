# Generated by Django 4.0.6 on 2022-08-17 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_inventoryitem_physical_serial_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemsonhand',
            name='date_registered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.0.6 on 2022-07-25 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rename_holder_key_holder_holder_techuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holder',
            name='holder_techuser',
        ),
    ]
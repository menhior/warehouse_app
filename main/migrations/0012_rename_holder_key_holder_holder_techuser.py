# Generated by Django 4.0.6 on 2022-07-25 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_holder_holder_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='holder',
            old_name='holder_key',
            new_name='holder_techuser',
        ),
    ]
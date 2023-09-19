# Generated by Django 4.0.6 on 2022-08-09 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_installation_reg_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='physical_serial_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.CreateModel(
            name='ItemsOnHand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_transfer', models.DateTimeField(auto_now_add=True)),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.techuser')),
                ('given_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.holder')),
                ('items_given', models.ManyToManyField(to='main.inventoryitem')),
            ],
        ),
    ]
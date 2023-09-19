from django.forms import ModelForm
from django import forms
from .models import InventoryItem, Installation, Alarm, ItemsOnHand

class InventoryItemForm(ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class ItemsOnHandForm(ModelForm):
    class Meta:
        model = ItemsOnHand
        fields = ['items_given', "given_to"]

class InstallationForm(ModelForm):
    class Meta:
        model = Installation
        fields = '__all__'

class AlarmStatusForm(ModelForm):
    class Meta:
        model = Alarm
        fields = ['checked']

class LimitedInventoryItemForm(ModelForm):
    registration_key_1 = forms.CharField(label = 'registration_key_1', required = False, ) 
    home_id_1 = forms.CharField(label = 'home_id_1', required = False)
    physical_serial_number_1 = forms.CharField(label = 'physical_serial_number_1', required = False)
    imei_1_1 = forms.CharField(label = 'imei_1_1', required = False) 
    imei_2_1 = forms.CharField(label = 'imei_2_1', required = False) 
    phone_number_1_1 = forms.CharField(label = 'phone_number_1_1', required = False) 
    phone_number_2_1 = forms.CharField(label = 'phone_number_2_1', required = False)

    registration_key_2 = forms.CharField(label = 'registration_key_2', required = False) 
    home_id_2 = forms.CharField(label = 'home_id_2', required = False)
    physical_serial_number_2 = forms.CharField(label = 'physical_serial_number_1', required = False)
    imei_1_2 = forms.CharField(label = 'imei_1_2', required = False) 
    imei_2_2 = forms.CharField(label = 'imei_2_2', required = False) 
    phone_number_1_2 = forms.CharField(label = 'phone_number_1_2', required = False) 
    phone_number_2_2 = forms.CharField(label = 'phone_number_2_2', required = False) 


    registration_key_3 = forms.CharField(label = 'registration_key_3', required = False) 
    home_id_3 = forms.CharField(label = 'home_id_3', required = False)
    physical_serial_number_3 = forms.CharField(label = 'physical_serial_number_1', required = False)
    imei_1_3 = forms.CharField(label = 'imei_1_3', required = False) 
    imei_2_3 = forms.CharField(label = 'imei_2_3', required = False) 
    phone_number_1_3 = forms.CharField(label = 'phone_number_1_3', required = False) 
    phone_number_2_3 = forms.CharField(label = 'phone_number_2_3', required = False) 
 
    registration_key_4 = forms.CharField(label = 'registration_key_4', required = False) 
    home_id_4 = forms.CharField(label = 'home_id_4', required = False)
    physical_serial_number_4 = forms.CharField(label = 'physical_serial_number_4', required = False)
    imei_1_4 = forms.CharField(label = 'imei_1_4', required = False) 
    imei_2_4 = forms.CharField(label = 'imei_2_4', required = False) 
    phone_number_1_4 = forms.CharField(label = 'phone_number_1_4', required = False) 
    phone_number_2_4 = forms.CharField(label = 'phone_number_2_4', required = False) 

    registration_key_5 = forms.CharField(label = 'registration_key_5', required = False) 
    home_id_5 = forms.CharField(label = 'home_id_5', required = False)
    physical_serial_number_5 = forms.CharField(label = 'physical_serial_number_5', required = False)
    imei_1_5 = forms.CharField(label = 'imei_1_5', required = False) 
    imei_2_5 = forms.CharField(label = 'imei_2_5', required = False) 
    phone_number_1_5 = forms.CharField(label = 'phone_number_1_5', required = False) 
    phone_number_2_5 = forms.CharField(label = 'phone_number_2_5', required = False) 

    registration_key_6 = forms.CharField(label = 'registration_key_6', required = False) 
    home_id_6 = forms.CharField(label = 'home_id_6', required = False)
    physical_serial_number_6 = forms.CharField(label = 'physical_serial_number_6', required = False)
    imei_1_6 = forms.CharField(label = 'imei_1_6', required = False) 
    imei_2_6 = forms.CharField(label = 'imei_2_6', required = False) 
    phone_number_1_6 = forms.CharField(label = 'phone_number_1_6', required = False) 
    phone_number_2_6 = forms.CharField(label = 'phone_number_2_6', required = False)

    registration_key_7 = forms.CharField(label = 'registration_key_7', required = False) 
    home_id_7 = forms.CharField(label = 'home_id_7', required = False)
    physical_serial_number_7 = forms.CharField(label = 'physical_serial_number_7', required = False)
    imei_1_7 = forms.CharField(label = 'imei_1_7', required = False) 
    imei_2_7 = forms.CharField(label = 'imei_2_7', required = False) 
    phone_number_1_7 = forms.CharField(label = 'phone_number_1_7', required = False) 
    phone_number_2_7 = forms.CharField(label = 'phone_number_2_7', required = False) 


    registration_key_8 = forms.CharField(label = 'registration_key_8', required = False) 
    home_id_8 = forms.CharField(label = 'home_id_8', required = False)
    physical_serial_number_8 = forms.CharField(label = 'physical_serial_number_8', required = False)
    imei_1_8 = forms.CharField(label = 'imei_1_8', required = False) 
    imei_2_8 = forms.CharField(label = 'imei_2_8', required = False) 
    phone_number_1_8 = forms.CharField(label = 'phone_number_1_8', required = False) 
    phone_number_2_8 = forms.CharField(label = 'phone_number_2_8', required = False) 
 
    registration_key_9 = forms.CharField(label = 'registration_key_9', required = False) 
    home_id_9 = forms.CharField(label = 'home_id_9', required = False)
    physical_serial_number_9 = forms.CharField(label = 'physical_serial_number_9', required = False)
    imei_1_9 = forms.CharField(label = 'imei_1_9', required = False) 
    imei_2_9 = forms.CharField(label = 'imei_2_1', required = False) 
    phone_number_1_9 = forms.CharField(label = 'phone_number_1_9', required = False) 
    phone_number_2_9 = forms.CharField(label = 'phone_number_2_9', required = False) 

    registration_key_10 = forms.CharField(label = 'registration_key_10', required = False) 
    home_id_10 = forms.CharField(label = 'home_id_10', required = False)
    physical_serial_number_10 = forms.CharField(label = 'physical_serial_number_10', required = False)
    imei_1_10 = forms.CharField(label = 'imei_1_10', required = False) 
    imei_2_10 = forms.CharField(label = 'imei_2_10', required = False) 
    phone_number_1_10 = forms.CharField(label = 'phone_number_1_10', required = False) 
    phone_number_2_10 = forms.CharField(label = 'phone_number_2_10', required = False)

    class Meta:
        model = InventoryItem
        fields = ['title', 'item_type', 'status', 'held_by', ]
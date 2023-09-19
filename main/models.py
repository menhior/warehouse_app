from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TechUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    email = models.CharField(max_length=25, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.name==None:
            return "ERROR-TECHUSER NAME IS NULL"
        return self.name

class Holder(models.Model):
    holder_name = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.holder_name

class ItemTitle(models.Model):
    item_name = models.CharField(max_length = 35)

    def __str__(self):
        return self.item_name

class ItemType(models.Model):
    type_name = models.CharField(max_length = 35)

    def __str__(self):
        return self.type_name


class InventoryItem(models.Model):

    STATUS = (
            ('Installed', 'Installed'),
            ('In hands of', 'In hands of'),
            ('Warehouse', 'Warehouse'),
            )

    title = models.ForeignKey(ItemTitle, on_delete=models.SET_NULL, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(TechUser, on_delete=models.SET_NULL, null=True, blank=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True)
    held_by = models.ForeignKey(Holder, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, choices=STATUS, default="Warehouse")
    registration_key = models.CharField(max_length=15, null=True, blank=True)
    home_id = models.CharField(max_length=15, null=True, blank=True)
    physical_serial_number = models.CharField(max_length=11, null=True, blank=True)
    depreciated_status = models.BooleanField(default=False)
    imei_1 = models.CharField(max_length=45, null=True, blank=True)
    imei_2 = models.CharField(max_length=45, null=True, blank=True)
    phone_number_1 = models.CharField(max_length=30, null=True, blank=True)
    phone_number_2 = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        if self.physical_serial_number!=None:
            return str(self.title.item_name + "# " + str(self.physical_serial_number)) or ''
        else:
            return str(self.title.item_name + "# " + str(self.id)) or ''



class Installation(models.Model):
    installation_date = models.DateTimeField(auto_now_add=True)
    items_used = models.ManyToManyField(InventoryItem)
    installed_by = models.ForeignKey(Holder, on_delete=models.SET_NULL, null=True)
    home_id = models.CharField(max_length=15, null=True)
    distance_in_km = models.FloatField(null=True, blank=True)
    uninstalled = models.BooleanField(default=False)


    def __str__(self):
        return str("Installation Number# " + str(self.id)) or ''

class Alarm(models.Model):
    where = models.CharField(max_length=75, null=True, blank=True)
    reg_key = models.CharField(max_length=15, null=True, blank=True)
    ph_serial_number = models.CharField(max_length=15, null=True, blank=True)
    error_to = models.ForeignKey(TechUser, on_delete=models.SET_NULL, null=True, blank=True)
    item_in_use = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        if self.item_in_use != None:
            return str(str(self.where) +"Item in Use: "+ str(self.item_in_use) + " # " + str(self.id)) or ''
        elif self.reg_key != None or self.ph_serial_number != None:
            return str(str(self.where) +"Registration Key: "+ str(self.reg_key) +" Physical Serial Number: "+ str(self.ph_serial_number) + " " + str(self.error_to) + " # " + str(self.id)) or ''
       


class ItemsOnHand(models.Model):
    date_of_transfer = models.DateTimeField(auto_now_add=True)
    items_given = models.ManyToManyField(InventoryItem)
    given_to = models.ForeignKey(Holder, on_delete=models.SET_NULL, null=True)
    given_by = models.ForeignKey(TechUser, on_delete=models.SET_NULL, null=True)
    related_file_name = models.CharField(max_length=50, null=True, blank=True)

from django.contrib import admin

from .models import TechUser, InventoryItem, ItemType, Holder, Installation, ItemTitle, Alarm, ItemsOnHand

# Register your models here.

admin.site.register(TechUser)
admin.site.register(InventoryItem)
admin.site.register(ItemType)
admin.site.register(Holder)
admin.site.register(Installation)
admin.site.register(ItemTitle)
admin.site.register(Alarm)
admin.site.register(ItemsOnHand)
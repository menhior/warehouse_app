"""m_inv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import indexView, inventoryList, technicianInventoryList, installationList, technicianInstallationList, installation, inventoryItem, loginPage, logoutUser, deleteInstall, deleteItem, createItem, createInstallation, updateItem, updateInstallation, alarmList, updateAlarm, technicianIndexView, technicianCreateInstallation, download_inventory_list_excel_data, download_installation_list_excel_data, bulkCreateInventoryItem

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name="logout"),
    path('', indexView, name = 'index_view'),
    path('inventory_list/', inventoryList, name='inventory_list'),
    path('installation_list/', installationList, name='installation_list'),
    path('installation/<str:pk>/', installation, name="installation"),
    path('inventory_item/<str:pk>/', inventoryItem, name="inventory_item"),
    path('item_create/', createItem, name="item_create"),
    path('item_bulk_create/', bulkCreateInventoryItem, name="item_bulk_create"),
    path('item_update/<str:pk>/', updateItem, name="item_update"),
    path('item_delete/<str:pk>/', deleteItem, name="item_delete"),
    path('installation_create/', createInstallation, name="installation_create"),
    path('installation_update/<str:pk>/', updateInstallation, name="installation_update"),
    path('installation_delete/<str:pk>/', deleteInstall, name="installation_delete"),
    path('alarm_list/', alarmList, name='alarm_list'),
    path('alarm_update/<str:pk>/', updateAlarm, name="alarm_update"),
    path('tech_dashboard/', technicianIndexView, name = 'tech_dashboard'),
    path('tech_inventory_list/', technicianInventoryList, name='tech_inventory_list'),
    path('tech_installation_list/', technicianInstallationList, name='tech_installation_list'),
    path('tech_installation_create/', technicianCreateInstallation, name="tech_installation_create"),
    path('inventory_list_excel_data/', download_inventory_list_excel_data, name="inventory_list_excel"),
    path('installation_list_excel_data/', download_installation_list_excel_data, name="installation_list_excel"),
    #path('items_on_hand_list/', itemsOnHandList, name="items_on_hand_list"),
    #path('items_on_hand_create/', createItemsOnHand, name="items_on_hand_create"),
]
import django_filters
from django_filters import DateFilter, CharFilter
from .models import InventoryItem, Installation



class InventoryListFilter(django_filters.FilterSet):
	
	serial_number = CharFilter(field_name='physical_serial_number', lookup_expr='icontains')
	registration_key = CharFilter(field_name='registration_key', lookup_expr='icontains')
	home_id = CharFilter(field_name='home_id', lookup_expr='icontains')
	
	class Meta:
		model = InventoryItem
		fields = '__all__'
		exclude = [ 'date_registered', 'physical_serial_number', 'registration_key', 'home_id', 'added_by']


class InstallationListFilter(django_filters.FilterSet):

	reg_key = CharFilter(field_name='reg_key', lookup_expr='icontains')
	home_id = CharFilter(field_name='home_id', lookup_expr='icontains')
	
	class Meta:
		model = Installation
		fields = '__all__'
		exclude = [ 'installation_date', 'items_used']

class TechnicianInventoryListFilter(django_filters.FilterSet):
	
	serial_number = CharFilter(field_name='physical_serial_number', lookup_expr='icontains')
	registration_key = CharFilter(field_name='registration_key', lookup_expr='icontains')
	home_id = CharFilter(field_name='home_id', lookup_expr='icontains')
	
	class Meta:
		model = InventoryItem
		fields = '__all__'
		exclude = [ 'date_registered', 'physical_serial_number', 'registration_key', 'home_id', 'held_by', 'added_by', 'depreciated_status']

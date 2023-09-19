from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import InventoryItem, ItemType, Installation, Alarm, TechUser, Holder, ItemsOnHand, ItemTitle, ItemType, Holder
from .filters import InventoryListFilter, InstallationListFilter, TechnicianInventoryListFilter
from .forms import InventoryItemForm, InstallationForm, AlarmStatusForm, LimitedInventoryItemForm, ItemsOnHandForm
from .decorators import allowed_users

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

import xlwt
from django.http import HttpResponse
import datetime

from odf import text, teletype
from odf.opendocument import load

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def indexView(request):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    inv_query = InventoryItem.objects.all().order_by('-date_registered')
    installed_count = inv_query.filter(status='Installed').count()
    in_hands_count = inv_query.filter(status='In hands of').count()
    warehouse_count = inv_query.filter(status='Warehouse').count()

    install_query = Installation.objects.all().order_by('-installation_date')[:5]

    total_inventory_count = InventoryItem.objects.all().count()

    types = ItemType.objects.all()
    types_name_list = []
    types_count_list = []
    types_url_list = []
    for type in types:
        types_name_list.append(str(type))
        types_count_list.append(InventoryItem.objects.all().filter(item_type=type).count())
        types_url_list.append("/inventory_list/?title=&added_by=&item_type="+str(type.id)+"&held_by=&status=&serial_number=&registration_key=&home_id=")

    full_types_list = zip(types_name_list, types_count_list,types_url_list)


    context = {"installed_count": installed_count, "in_hands_count": in_hands_count, "warehouse_count": warehouse_count,
     "install_query": install_query, "full_types_list": full_types_list, "total_inventory_count": total_inventory_count, "unchecked_alarms_count": unchecked_alarms_count }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def inventoryList(request):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    inv_query = InventoryItem.objects.all().order_by('-date_registered')

    InventoryFilter = InventoryListFilter(request.GET, queryset=inv_query)
    inv_query = InventoryFilter.qs 

    inventory_count = inv_query.count()

    paginator = Paginator(inv_query, 100)
    page = request.GET.get('page', 1)

    try:
        inv_items = paginator.page(page)
    except PageNotAnInteger:
        inv_items = paginator.page(1)
    except EmptyPage:
        inv_items = paginator.page(paginator.num_pages)

    context = {"InventoryFilter": InventoryFilter, "inv_items": inv_items, 'paginator': paginator, "unchecked_alarms_count": unchecked_alarms_count, 'inventory_count': inventory_count,}
    return render(request, 'inventory_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def installationList(request):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    install_query = Installation.objects.all().order_by('-installation_date')

    InstallationFilter = InstallationListFilter(request.GET, queryset=install_query)
    install_query = InstallationFilter.qs 

    installations_count = install_query.count()

    paginator = Paginator(install_query, 100)
    page = request.GET.get('page', 1)


    try:
        installations = paginator.page(page)
    except PageNotAnInteger:
        installations = paginator.page(1)
    except EmptyPage:
        installations = paginator.page(paginator.num_pages)

    context = {"installations": installations, 'InstallationFilter': InstallationFilter, "paginator": paginator, "unchecked_alarms_count": unchecked_alarms_count, 'installations_count': installations_count}
    return render(request, 'installation_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def installation(request, pk):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    installation = Installation.objects.get(id=pk)

    context = {'installation': installation, "unchecked_alarms_count": unchecked_alarms_count}
    return render(request, 'installation.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def inventoryItem(request, pk):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    inventory_item = InventoryItem.objects.get(id=pk)
    item_installs = inventory_item.installation_set.all()
    context = {'inventory_item': inventory_item, "item_installs": item_installs, "unchecked_alarms_count": unchecked_alarms_count}
    return render(request, 'inventory_item.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index_view')
        print(hello)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password=password)


            if user is not None:
                login(request, user)
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                else:
                    return render(request, 'group_not_fitting.html')
                if group == 'Inventorizer':
                    return redirect('index_view')
                elif group == 'Technician':
                    return redirect('tech_dashboard')
                else:
                    return render(request, 'login.html')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context  = {}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def createItem(request):
    tech_user = TechUser.objects.get(user=request.user)
    print(tech_user)
    all_items_list = InventoryItem.objects.all()
    form = InventoryItemForm()
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            if form.instance.registration_key !=None and form.instance.physical_serial_number != None:
                if len(form.instance.registration_key) > 6 and len(form.instance.physical_serial_number) == 11:
                    serial_number_match_count = InventoryItem.objects.filter(physical_serial_number= form.instance.physical_serial_number).count()
                    key_match_count = InventoryItem.objects.filter(registration_key= form.instance.registration_key).count()
                    if key_match_count == 0 or serial_number_match_count == 0:
                        form.instance.added_by = tech_user
                        if form.instance.held_by != None and form.instance.status == "Warehouse":
                            form.instance.status = "In hands of"
                            item = form.save()
                            return redirect('index_view')
                        elif form.instance.held_by == None and form.instance.status != "Warehouse":
                            form.instance.status = "Warehouse"
                            item = form.save()
                            return redirect('index_view')
                        else:
                            item = form.save()
                            return redirect('index_view')
                    else:
                        Alarm.objects.create(where="Failed Creation due to existance of same Key or S/N: ", reg_key = form.instance.registration_key, ph_serial_number = form.instance.physical_serial_number, error_to=tech_user)
                        return redirect('index_view')
                else:
                    Alarm.objects.create(where="Failed Creation due to Lenght of Key or S/N: ", reg_key = form.instance.registration_key, ph_serial_number = form.instance.physical_serial_number, error_to=tech_user)  
                    return redirect('index_view')
            else:
                form.instance.added_by = tech_user
                if form.instance.held_by != None and form.instance.status == "Warehouse":
                    form.instance.status = "In hands of"
                    item = form.save()
                    return redirect('index_view')
                elif form.instance.held_by == None and form.instance.status != "Warehouse":
                    form.instance.status = "Warehouse"
                    item = form.save()
                    return redirect('index_view')
                else:
                    item = form.save()
                    return redirect('index_view')

    context = {'form':form,}
    return render(request, 'inventory_item_create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def updateItem(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    form = InventoryItemForm(instance=item)
    tech_user = TechUser.objects.get(user=request.user)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            if form.instance.registration_key !=None and form.instance.physical_serial_number != None:
                if len(form.instance.registration_key) > 6 and len(form.instance.physical_serial_number) == 11:
                    if form.instance.held_by != None and form.instance.status == "Warehouse":
                        form.instance.status = "In hands of"
                        item = form.save()
                        return redirect('index_view')
                    elif form.instance.held_by == None and form.instance.status != "Warehouse":
                        form.instance.status = "Warehouse"
                        item = form.save()
                        return redirect('index_view')
                    else:
                        item = form.save()
                        return redirect('index_view')
                else:
                    Alarm.objects.create(where="Failed Update due to Lenght of Key or S/N: ", reg_key = form.instance.registration_key, ph_serial_number = form.instance.physical_serial_number, error_to=tech_user)  
                    return redirect('index_view')
            else:
                if form.instance.held_by != None and form.instance.status == "Warehouse":
                    form.instance.status = "In hands of"
                    item = form.save()
                    return redirect('index_view')
                elif form.instance.held_by == None and form.instance.status != "Warehouse":
                    form.instance.status = "Warehouse"
                    item = form.save()
                    return redirect('index_view')
                else:
                    item = form.save()
                    return redirect('index_view')

    context = {'form':form}
    return render(request, 'inventory_item_update.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def deleteItem(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect('index_view')

    context = {'item': item}
    return render(request, 'inventory_item_delete.html', context)

@login_required(login_url='login')
def createInstallation(request):
    items_in_warehouse = InventoryItem.objects.filter(status="Warehouse")
    items_on_hands = InventoryItem.objects.filter(status="In hands of")
    print(items_in_warehouse)
    print(items_on_hands)
    form = InstallationForm()
    tech_user = TechUser.objects.get(user=request.user)
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = InstallationForm(request.POST)
        if form.is_valid():
            installation = form.save()
            for item in installation.items_used.all():
                print(item)
                if item.status == "Installed":
                    Alarm.objects.create(where="Failed Installation due to one of items listed already being in use: ", item_in_use = item,  reg_key = form.instance.reg_key, error_to=tech_user)
                    installation.delete()
                    break
                else:
                    item.status = "Installed"
                    item.home_id = installation.home_id
                    item.held_by = installation.installed_by
                    print(item.status)
                    item.save()
            return redirect('index_view')

    context = {'form':form, 'items_in_warehouse': items_in_warehouse, 'items_on_hands': items_on_hands}
    return render(request, 'installation_create.html', context)

@login_required(login_url='login')
def updateInstallation(request, pk):
    tech_user = TechUser.objects.get(user=request.user)
    installation = get_object_or_404(Installation, pk=pk)
    form = InstallationForm(instance=installation)
    if request.method == 'POST':
        form = InstallationForm(request.POST, instance=installation)
        if form.is_valid():
            if form.instance.reg_key != None:
                if len(form.instance.reg_key) > 6:
                    installation = form.save()
                    for item in installation.items_used.all():
                        if item.status == "Installed":
                            Alarm.objects.create(where="Failed Installation due to one of items listed already being in use: ", item_in_use = item,  reg_key = form.instance.reg_key, error_to=tech_user)
                            break
                        else:
                            item.status = "Installed"
                            item.home_id = installation.home_id
                            item.held_by = installation.installed_by
                            item.save()
                            return redirect('index_view')
                    return redirect('index_view')
                else:
                    Alarm.objects.create(where="Failed Installation due to Registration Key being too short: ", reg_key = form.instance.reg_key, error_to=tech_user)  
                    return redirect('index_view')
            else:
                installation = form.save()
                for item in installation.items_used.all():
                    if item.status == "Installed":
                        Alarm.objects.create(where="Failed Installation due to one of items listed already being in use: ", item_in_use = item,  reg_key = form.instance.reg_key, error_to=tech_user)
                        break
                    else:
                        item.status = "Installed"
                        item.home_id = installation.home_id
                        item.held_by = installation.installed_by
                        item.save()
                        return redirect('index_view')
                return redirect('index_view')

    context = {'form':form}
    return render(request, 'installation_update.html', context)



@login_required(login_url='login')
def deleteInstall(request, pk):
    install = get_object_or_404(Installation, pk=pk)
    if request.method == "POST":
        install.delete()
        return redirect('index_view')

    context = {'install': install}
    return render(request, 'installation_delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def alarmList(request):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    alarms = Alarm.objects.filter(checked=False, error_to=tech_user)
    context = {'alarms': alarms, 'unchecked_alarms_count': unchecked_alarms_count}
    return render(request, 'alarm_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Inventorizer"])
def updateAlarm(request, pk):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    alarm = get_object_or_404(Alarm, pk=pk)
    form = AlarmStatusForm(instance=alarm)
    if request.method == 'POST':
        form = AlarmStatusForm(request.POST, instance=alarm)
        alarm = form.save()
        return redirect('index_view')
    context = {'form': form, 'unchecked_alarms_count': unchecked_alarms_count}
    return render(request, 'alarm_update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["Technician"])
def technicianIndexView(request):
    tech_user = TechUser.objects.get(user=request.user)
    holder = Holder.objects.filter(holder_name=tech_user.name)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    inv_query = InventoryItem.objects.filter(held_by=holder[0]).order_by('-date_registered')
    installed_count = inv_query.filter(status='Installed').count()
    in_hands_count = inv_query.filter(status='In hands of').count()
    warehouse_count = inv_query.filter(status='Warehouse').count()

    install_query = Installation.objects.filter(installed_by=holder[0]).order_by('-installation_date')[:5]

    total_inventory_count = InventoryItem.objects.filter(held_by=holder[0]).count()

    types = ItemType.objects.all()
    types_name_list = []
    types_count_list = []
    types_url_list = []
    for type in types:
        types_name_list.append(str(type))
        types_count_list.append(InventoryItem.objects.all().filter(item_type=type).count())
        types_url_list.append("/inventory_list/?title=&added_by=&item_type="+str(type.id)+"&held_by=&status=&serial_number=&registration_key=&home_id=")

    full_types_list = zip(types_name_list, types_count_list,types_url_list)


    context = {"installed_count": installed_count, "in_hands_count": in_hands_count, "warehouse_count": warehouse_count,
     "install_query": install_query, "full_types_list": full_types_list, "total_inventory_count": total_inventory_count, "unchecked_alarms_count": unchecked_alarms_count }
    return render(request, 'technician_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=["Technician"])
def technicianInventoryList(request):
    tech_user = TechUser.objects.get(user=request.user)
    holder = Holder.objects.filter(holder_name=tech_user.name)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    inv_query = InventoryItem.objects.filter(held_by=holder[0]).order_by('-date_registered')

    InventoryFilter = TechnicianInventoryListFilter(request.GET, queryset=inv_query)
    inv_query = InventoryFilter.qs 

    paginator = Paginator(inv_query, 100)
    page = request.GET.get('page', 1)

    try:
        inv_items = paginator.page(page)
    except PageNotAnInteger:
        inv_items = paginator.page(1)
    except EmptyPage:
        inv_items = paginator.page(paginator.num_pages)

    context = {"InventoryFilter": InventoryFilter, "inv_items": inv_items, 'paginator': paginator, "unchecked_alarms_count": unchecked_alarms_count}
    return render(request, 'technician_inventory_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=["Technician"])
def technicianInstallationList(request):
    tech_user = TechUser.objects.get(user=request.user)
    holder = Holder.objects.filter(holder_name=tech_user.name)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    install_query = Installation.objects.filter(installed_by=holder[0]).order_by('-installation_date')

    InstallationFilter = InstallationListFilter(request.GET, queryset=install_query)
    install_query = InstallationFilter.qs 

    paginator = Paginator(install_query, 100)
    page = request.GET.get('page', 1)

    try:
        installations = paginator.page(page)
    except PageNotAnInteger:
        installations = paginator.page(1)
    except EmptyPage:
        installations = paginator.page(paginator.num_pages)

    context = {"installations": installations, 'InstallationFilter': InstallationFilter, "paginator": paginator, "unchecked_alarms_count": unchecked_alarms_count}
    return render(request, 'technician_installation_list.html', context)


@login_required(login_url='login')
def technicianCreateInstallation(request):
    form = InstallationForm()
    tech_user = TechUser.objects.get(user=request.user)
    holder = Holder.objects.filter(holder_name=tech_user.name)
    holder_item_query = InventoryItem.objects.filter(held_by=holder[0], status='In hands of')
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = InstallationForm(request.POST)
        if form.is_valid():
            if form.instance.reg_key != None:
                if len(form.instance.reg_key) > 6:
                    form.instance.installed_by = holder[0]
                    installation = form.save()
                    for item in installation.items_used.all():
                        if item.status == "Installed":
                            Alarm.objects.create(where="Failed Installation due to one of items listed already being in use: ", item_in_use = item,  reg_key = form.instance.reg_key, error_to=tech_user)
                            installation.delete()
                            break
                        else:
                            item.status = "Installed"
                            item.home_id = installation.home_id
                            item.held_by = installation.installed_by
                            item.save()
                            return redirect('tech_dashboard')
                    return redirect('tech_dashboard')
                else:
                    Alarm.objects.create(where="Failed Installation due to Registration Key being too short: ", reg_key = form.instance.reg_key, error_to=tech_user)  
                    return redirect('tech_dashboard')
            else:
                form.instance.installed_by = holder[0]
                installation = form.save()
                for item in installation.items_used.all():
                    if item.status == "Installed":
                        Alarm.objects.create(where="Failed Installation due to one of items listed already being in use: ", item_in_use = item,  reg_key = form.instance.reg_key, error_to=tech_user)
                        installation.delete()
                        break
                    else:
                        item.status = "Installed"
                        item.home_id = installation.home_id
                        item.held_by = installation.installed_by
                        item.save()
                        return redirect('tech_dashboard')
                return redirect('tech_dashboard')


    context = {'form':form, 'holder_item_query': holder_item_query,}
    return render(request, 'technician_installation_create.html', context)

def download_inventory_list_excel_data(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="Inventory_Item_List.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['Title', 'Date Registered', 'Added by', 'Item Type', 'Title', 'In hands of ', 'Status', 'Registration Key','Home Id', 'Physical S/N', 'Depreciation Status', 'IMEI 1', 'IMEI 2','Phone Number 1','Phone Number 2',]

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    data = InventoryItem.objects.all() #dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, str(my_row.title), font_style)
        ws.write(row_num, 1, str(my_row.date_registered), font_style)
        ws.write(row_num, 2, str(my_row.added_by), font_style)
        ws.write(row_num, 3, str(my_row.item_type), font_style)
        ws.write(row_num, 4, str(my_row.held_by), font_style)
        ws.write(row_num, 5, str(my_row.status), font_style)
        ws.write(row_num, 6, str(my_row.registration_key), font_style)
        ws.write(row_num, 7, str(my_row.home_id), font_style)
        ws.write(row_num, 8, str(my_row.physical_serial_number), font_style)
        ws.write(row_num, 9, str(my_row.depreciated_status), font_style)
        ws.write(row_num, 10, str(my_row.imei_1), font_style)
        ws.write(row_num, 11, str(my_row.imei_2), font_style)
        ws.write(row_num, 12, str(my_row.phone_number_1), font_style)
        ws.write(row_num, 13, str(my_row.phone_number_2), font_style)
    wb.save(response)
    return response

def download_installation_list_excel_data(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="Installation_List.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['Installation Date', 'Items Used', 'Installed By', 'Home Id', 'Distance Passed(in km)', 'Uninstalled Status ']

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    data = Installation.objects.all() #dummy method to fetch data.
    for my_row in data:
        items_used_string = ""
        print(my_row.items_used.all())
        for item in my_row.items_used.all():
                items_used_string += str(item) + ", \n"

        row_num = row_num + 1
        ws.write(row_num, 0, str(my_row.installation_date), font_style)
        ws.write(row_num, 1, items_used_string, font_style)
        ws.write(row_num, 2, str(my_row.installed_by), font_style)
        ws.write(row_num, 3, str(my_row.home_id), font_style)
        ws.write(row_num, 4, str(my_row.distance_in_km), font_style)
        ws.write(row_num, 5, str(my_row.uninstalled), font_style)
    wb.save(response)
    return response

def bulkCreateInventoryItem(request):
    tech_user = TechUser.objects.get(user=request.user)
    form = LimitedInventoryItemForm()
    if request.method == 'POST':
        form = LimitedInventoryItemForm(request.POST)
        title = ItemTitle.objects.filter(id=request.POST.get('title', 'None'))
        item_type = ItemType.objects.filter(id=request.POST.get('item_type', 'None'))
        holder = request.POST.get('held_by', 'None')
        if holder == "":
            holder = None
        else:
            holder = Holder.objects.filter(id=holder)
            holder = holder[0]
        
        
        if form.is_valid() and str(item_type[0]) == "Meter":
            form.instance.added_by = tech_user
            if holder != None and form.instance.status == "Warehouse":
                form.instance.status = "In hands of"
            elif holder == None and form.instance.status != "Warehouse":
                form.instance.status = "Warehouse"
            registration_key_1 = request.POST.get('registration_key_1', 'None')
            registration_key_2 = request.POST.get('registration_key_2', 'None')
            registration_key_3 = request.POST.get('registration_key_3', 'None')
            registration_key_4 = request.POST.get('registration_key_4', 'None')
            registration_key_5 = request.POST.get('registration_key_5', 'None')
            registration_key_6 = request.POST.get('registration_key_6', 'None')
            registration_key_7 = request.POST.get('registration_key_7', 'None')
            registration_key_8 = request.POST.get('registration_key_8', 'None')
            registration_key_9 = request.POST.get('registration_key_9', 'None')
            registration_key_10 = request.POST.get('registration_key_10', 'None')
            home_id_1 = request.POST.get('home_id_1', 'None')
            home_id_2 = request.POST.get('home_id_2', 'None')
            home_id_3 = request.POST.get('home_id_3', 'None')
            home_id_4 = request.POST.get('home_id_4', 'None')
            home_id_5 = request.POST.get('home_id_5', 'None')
            home_id_6 = request.POST.get('home_id_6', 'None')
            home_id_7 = request.POST.get('home_id_7', 'None')
            home_id_8 = request.POST.get('home_id_8', 'None')
            home_id_9 = request.POST.get('home_id_9', 'None')
            home_id_10 = request.POST.get('home_id_10', 'None')
            physical_serial_number_1 = request.POST.get('physical_serial_number_1', 'None')
            physical_serial_number_2 = request.POST.get('physical_serial_number_2', 'None')
            physical_serial_number_3 = request.POST.get('physical_serial_number_3', 'None')
            physical_serial_number_4 = request.POST.get('physical_serial_number_4', 'None')
            physical_serial_number_5 = request.POST.get('physical_serial_number_5', 'None')
            physical_serial_number_6 = request.POST.get('physical_serial_number_6', 'None')
            physical_serial_number_7 = request.POST.get('physical_serial_number_7', 'None')
            physical_serial_number_8 = request.POST.get('physical_serial_number_8', 'None')
            physical_serial_number_9 = request.POST.get('physical_serial_number_9', 'None')
            physical_serial_number_10 = request.POST.get('physical_serial_number_10', 'None')
            imei_1_1 = request.POST.get('imei_1_1', 'None')
            imei_1_2 = request.POST.get('imei_1_2', 'None')
            imei_1_3 = request.POST.get('imei_1_3', 'None')
            imei_1_4 = request.POST.get('imei_1_4', 'None')
            imei_1_5 = request.POST.get('imei_1_5', 'None')
            imei_1_6 = request.POST.get('imei_1_6', 'None')
            imei_1_7 = request.POST.get('imei_1_7', 'None')
            imei_1_8 = request.POST.get('imei_1_8', 'None')
            imei_1_9 = request.POST.get('imei_1_9', 'None')
            imei_1_10 = request.POST.get('imei_1_10', 'None')
            imei_2_1 = request.POST.get('imei_2_1', 'None')
            imei_2_2 = request.POST.get('imei_2_2', 'None')
            imei_2_3 = request.POST.get('imei_2_3', 'None')
            imei_2_4 = request.POST.get('imei_2_4', 'None')
            imei_2_5 = request.POST.get('imei_2_5', 'None')
            imei_2_6 = request.POST.get('imei_2_6', 'None')
            imei_2_7 = request.POST.get('imei_2_7', 'None')
            imei_2_8 = request.POST.get('imei_2_8', 'None')
            imei_2_9 = request.POST.get('imei_2_9', 'None')
            imei_2_10 = request.POST.get('imei_2_10', 'None')
            phone_number_1_1 = request.POST.get('phone_number_1_1', 'None')
            phone_number_1_2 = request.POST.get('phone_number_1_2', 'None')
            phone_number_1_3 = request.POST.get('phone_number_1_3', 'None')
            phone_number_1_4 = request.POST.get('phone_number_1_4', 'None')
            phone_number_1_5 = request.POST.get('phone_number_1_5', 'None')
            phone_number_1_6 = request.POST.get('phone_number_1_6', 'None')
            phone_number_1_7 = request.POST.get('phone_number_1_7', 'None')
            phone_number_1_8 = request.POST.get('phone_number_1_8', 'None')
            phone_number_1_9 = request.POST.get('phone_number_1_9', 'None')
            phone_number_1_10 = request.POST.get('phone_number_1_10', 'None')
            phone_number_2_1 = request.POST.get('phone_number_2_1', 'None')
            phone_number_2_2 = request.POST.get('phone_number_2_2', 'None')
            phone_number_2_3 = request.POST.get('phone_number_2_3', 'None')
            phone_number_2_4 = request.POST.get('phone_number_2_4', 'None')
            phone_number_2_5 = request.POST.get('phone_number_2_5', 'None')
            phone_number_2_6 = request.POST.get('phone_number_2_6', 'None')
            phone_number_2_7 = request.POST.get('phone_number_2_7', 'None')
            phone_number_2_8 = request.POST.get('phone_number_2_8', 'None')
            phone_number_2_9 = request.POST.get('phone_number_2_9', 'None')
            phone_number_2_10 = request.POST.get('phone_number_2_10', 'None')
            
            aux_cable = ItemTitle.objects.filter(item_name="AUX Cable")
            aux_cable = aux_cable[0]
            microphone = ItemTitle.objects.filter(item_name="Microfon")
            microphone = microphone[0]
            aux_rca_cable = ItemTitle.objects.filter(item_name="AUX to RCA cable")
            aux_rca_cable = aux_rca_cable[0]
            electric_extension_cord = ItemTitle.objects.filter(item_name="Electric Extension Cord")
            electric_extension_cord = electric_extension_cord[0]
            batteries = ItemTitle.objects.filter(item_name="Batteries")
            batteries = batteries[0]

            cable_type = ItemType.objects.filter(type_name="Cable")
            cable_type = cable_type[0]
            consumable_type = ItemType.objects.filter(type_name="Consumable")
            consumable_type = consumable_type[0]

            InventoryItem.objects.bulk_create([
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_1, home_id=home_id_1, physical_serial_number=physical_serial_number_1, imei_1=imei_1_1, imei_2=imei_2_1, phone_number_1=phone_number_1_1, phone_number_2=phone_number_2_1 ),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_2, home_id=home_id_2, physical_serial_number=physical_serial_number_2, imei_1=imei_1_2, imei_2=imei_2_2, phone_number_1=phone_number_1_2, phone_number_2=phone_number_2_2),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_3, home_id=home_id_3, physical_serial_number=physical_serial_number_3, imei_1=imei_1_3, imei_2=imei_2_3, phone_number_1=phone_number_1_3, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_4, home_id=home_id_4, physical_serial_number=physical_serial_number_4, imei_1=imei_1_4, imei_2=imei_2_4, phone_number_1=phone_number_1_4, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_5, home_id=home_id_5, physical_serial_number=physical_serial_number_5, imei_1=imei_1_5, imei_2=imei_2_5, phone_number_1=phone_number_1_5, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_6, home_id=home_id_6, physical_serial_number=physical_serial_number_6, imei_1=imei_1_6, imei_2=imei_2_6, phone_number_1=phone_number_1_6, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_7, home_id=home_id_7, physical_serial_number=physical_serial_number_7, imei_1=imei_1_7, imei_2=imei_2_7, phone_number_1=phone_number_1_7, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_8, home_id=home_id_8, physical_serial_number=physical_serial_number_8, imei_1=imei_1_8, imei_2=imei_2_8, phone_number_1=phone_number_1_8, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_9, home_id=home_id_9, physical_serial_number=physical_serial_number_9, imei_1=imei_1_9, imei_2=imei_2_9, phone_number_1=phone_number_1_9, phone_number_2=phone_number_2_1),
                  InventoryItem(title=title[0], status=form.instance.status, added_by=tech_user, held_by=holder, item_type=item_type[0], registration_key=registration_key_10, home_id=home_id_10, physical_serial_number=physical_serial_number_10, imei_1=imei_1_10, imei_2=imei_2_10, phone_number_1=phone_number_1_10, phone_number_2=phone_number_2_1),
                ])
            InventoryItem.objects.bulk_create([
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder ),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                ])
            InventoryItem.objects.bulk_create([
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder ),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=aux_rca_cable, added_by=tech_user, item_type=cable_type, status=form.instance.status, held_by=holder),
                ])
            InventoryItem.objects.bulk_create([
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder ),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=electric_extension_cord, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                ])
            InventoryItem.objects.bulk_create([
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder ),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                  InventoryItem(title=batteries, added_by=tech_user, item_type=consumable_type, status=form.instance.status, held_by=holder),
                ])
        else:
            pass
        return redirect('index_view')

    context = {'form':form,}
    return render(request, 'bulk_meter_create.html', context)


'''def itemsOnHandList(request):
    tech_user = TechUser.objects.get(user=request.user)
    unchecked_alarms_count = Alarm.objects.filter(checked=False, error_to=tech_user).count()
    items_on_hand_query = ItemsOnHand.objects.all().order_by('-date_of_transfer')

    ItemsOnHandListFilter = ItemsOnHandListFilter(request.GET, queryset=items_on_hand_query)
    items_on_hand_query = ItemsOnHandListFilter.qs 

    items_on_hand_count = items_on_hand_query.count()

    paginator = Paginator(items_on_hand_query, 100)
    page = request.GET.get('page', 1)


    try:
        items_on_hand = paginator.page(page)
    except PageNotAnInteger:
        items_on_hand = paginator.page(1)
    except EmptyPage:
        items_on_hand = paginator.page(paginator.num_pages)

    #context = {"items_on_hand": items_on_hand, 'ItemsOnHandListFilter': ItemsOnHandListFilter, "paginator": paginator, "unchecked_alarms_count": unchecked_alarms_count, 'items_on_hand_count': items_on_hand_count}
    context = {"items_on_hand": items_on_hand, "paginator": paginator, "unchecked_alarms_count": unchecked_alarms_count, }
    return render(request, 'items_on_hand_list.html', context)

def createItemsOnHand(request):
    tech_user = TechUser.objects.get(user=request.user)
    all_items_list = InventoryItem.objects.all()
    form = ItemsOnHandForm()
    if request.method == 'POST':
        form = ItemsOnHandForm(request.POST)
        if form.is_valid():
            tehvil = form.save()
            tehvil_date = tehvil.date_of_transfer.strftime('%d-%m-%y')
            tehvil.related_file_name = "Təhvil_" +str(tehvil_date)
            print(tehvil.related_file_name)
        
        return redirect('index_view')

    context = {'form': form,}
    return render(request, 'items_on_hand_create.html', context)'''
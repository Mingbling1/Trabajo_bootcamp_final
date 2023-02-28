from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ContactForm, ContactFormW
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
import requests
import threading
import time
# %b. %d, 
def chart_data(request):
  orders = Order.objects.all().order_by('-date')[:10][::-1]
  labels = [timezone.localtime(order.date).strftime('%I:%M:%S %p') for order in orders]
  data_compra = [order.tc_compra for order in orders]
  data_venta = [order.tc_venta for order in orders]
  return JsonResponse({'labels': labels, 'data_compra': data_compra, 'data_venta': data_venta})

def order_count(request):
    count = Order.objects.count()
    return JsonResponse({'count': count})
# Create your views here.

def crear_json():
    data = requests.post("https://app.rextie.com/api/v1/fxrates/rate/?origin=template-original&commit=false", headers={
    "Host": "app.rextie.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.rextie.com/",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "75",
    "Origin": "https://www.rextie.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",},json={"source_currency":"PEN","target_currency":"USD","source_amount":"1.00"})
    data_json = [{"model": "main.order", 
    "pk": (Order.objects.all().count()+1), 
    "fields": { 'fx_rate_buy': float(data.json()['fx_rate_buy']), 'fx_rate_sell': float(data.json()['fx_rate_sell']) }}]
    return data_json
# Tarea a ejecutarse cada determinado tiempo.
def timer():
    while True:
        time.sleep(60)
        print("Añadiendo Orden")
        tc = crear_json()[0]
        order = Order.objects.create(
        tc_compra= tc['fields']['fx_rate_buy'],
        tc_venta=tc['fields']['fx_rate_sell'],)
        order.save()
        print('actualizando')
        
        
@login_required
def order(request):
    orders_list = Order.objects.all().order_by('-date')
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    orders = Order.objects.all().order_by('-date')
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    if request.method =='POST':
        form = ContactFormW(request.POST)
        if form.is_valid():
            #obj = form.save(commit=False)
            print("*ENVIANDO MENSAJE*")
            data = requests.post("https://app.rextie.com/api/v1/fxrates/rate/?origin=template-original&commit=false", 
            headers={
                    "Host": "app.rextie.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": "https://www.rextie.com/",
                    "Content-Type": "application/json; charset=UTF-8",
                    "Content-Length": "75",
                    "Origin": "https://www.rextie.com",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    },
            json={"source_currency":"PEN","target_currency":"USD","source_amount":"1.00"})
            tcCompra = data.json().get('fx_rate_buy')
            tcVenta = data.json().get('fx_rate_sell')
            numero = request.POST.get("numero", "921099315")
            mensaje = "El tipo de cambio (Compra) del $USD es: "+tcCompra+" y la Venta es: "+tcVenta
            print(mensaje)
            r = requests.get("https://apis.tecnytte.com:8083/sendMessagesTELWAP?mensaje="+mensaje+"&whatsapp=51"+numero+"&token=yfwwsedrftgyhujikolpasxxcvbddsd")
            return redirect("dashboard-order-paginated")  
    form = ContactFormW()
    context = { 
        'form': form,
        'orders': orders,
        'page_obj': page_obj,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request,"dashboard/order.html", context)
    #return HttpResponse("This is the Staff Page")

@login_required
def index(request):
    usuarios = User.objects.all()
    for usuario in usuarios:
        print(usuario.profile.phone)
    product = Product.objects.all()
    product_count = product.count()
    ordenes = Order.objects.all().order_by('-date')[:10][::-1]
    orders = Order.objects.all()
    orders_count = orders.count()
    customer = User.objects.filter()
    customer_count = customer.count()
    if request.method =='POST':
        print('POST')
        return redirect('dashboard-order')   
    else:
        print('get')
        form = OrderForm()
        context = {
            'form': form,
            'products': product,
            'product_count': product_count,
            'workers_count': customer_count,
            'orders': ordenes,
            'orders_count': orders_count,             
        }
        t = threading.Thread(target=timer)
        t.start()      

    return render(request,"dashboard/index.html", context)
    #return HttpResponse("<h1 style=""color:green;""> This is the Index Page </h1>")

@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers': workers,
        'workers_count':workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
         }
    return render(request,"dashboard/staff.html", context)
    #return HttpResponse("This is the Staff Page")

@login_required
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def product(request):
    items = Product.objects.all() # Using ORM
    product_count = items.count()
   #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count
    }
    return render(request, 'dashboard/product.html', context)
    #return HttpResponse("This is the Staff Page")

@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method== 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_calid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context={
        'form': form,
    }
    return render(request, 'dashboard/product_update.html', context)


@login_required
def contact_view(request):
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})



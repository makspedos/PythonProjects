from django.template import loader

from .forms import CustomersForm
from django.shortcuts import render
from .models import *
from .forms import CheckoutBuyerForm

from django.http import JsonResponse

def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    return render(request ,'myShop/home.html', locals())


def index(request):
    latest_question_list = Product.objects.order_by('-product_id')[:10]
    context = {'latest_question_list': latest_question_list,}
    template = loader.get_template('myShop/index.html')
    return render(request, 'myShop/index.html' , context)


def product(request, id):
    product = Product.objects.get(product_id=id)
    session_key= request.session.session_key
    categories_list = ProductCategory.objects.order_by('name')
    if not session_key:
        request.session.cycle_key()
    print(request.session.session_key)

    return render(request, 'myShop/product.html', locals())


def official(request):
    return render(request, 'myShop/official.html')


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = Basket.objects.filter(session_key=session_key, is_active=True)
    price_for_order = 0
    form = CheckoutBuyerForm(request.POST or None)
    for product in products_in_basket:
        price_for_order+=product.total_price

    if request.POST:
        if form.is_valid():
            print('Yes')
            data = request.POST
            number = data["number"]
            name = data["name"]
            last_name = data["last_name"]
            customer, created = Customers.objects.get_or_create(name=name, number=number, last_name=last_name)
        else:
            print('No')

    return render(request, 'myShop/checkout.html', locals())


def register(request):
    form = CustomersForm(request.POST or None)
    name = Customers.name
    last_name = Customers.last_name
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data
        print(data['name'])
        form = form.save()
    return render(request, 'myShop/register.html', locals())


def login(request):
    form = CustomersForm(request.POST or None)
    name = Customers.name
    last_name = Customers.last_name
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data
        print(data['name'])
        form = form.save()
    return render(request, 'myShop/login.html', locals())


def basket(request):
    return_dict = {}
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    number = data.get("number")
    is_delete = data.get("is_delete")

    if is_delete== 'true':
        Basket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = Basket.objects.get_or_create(session_key=session_key, product_id = product_id ,is_active=True,defaults={"count":number})
        if not created:
            new_product.count += int(number)
            new_product.save(force_update=True)

    products_in_basket = Basket.objects.filter(session_key=session_key, is_active=True)
    product_total_count = products_in_basket.count()
    return_dict["products_total_count"] = product_total_count

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["product_name"] = item.product.product_name
        product_dict["total_price"] = item.total_price
        product_dict["count"] = item.count
        return_dict["products"].append(product_dict)
    return JsonResponse(return_dict)


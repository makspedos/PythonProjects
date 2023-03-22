from django.template import loader
from django.views import View

from .forms import CustomersForm
from django.shortcuts import render
from .models import *
from .forms import CheckoutBuyerForm

from django.http import JsonResponse, HttpResponseRedirect

class Index(View):
    def get(self, request):
        return HttpResponseRedirect(f'/home{request.get_full_path()[1:]}')
def home(request):
    categories =ProductCategory.objects.all()
    categoryID = request.GET.get('category')
    brand_name=request.GET.get('brand')
    all_products =ProductImage.objects.filter(is_active=True, is_main=True)
    products_images=None
    if brand_name:
        products_images = ProductImage.objects.filter(product__brand=brand_name)
    if categoryID:
        products_images = ProductImage.objects.filter(product__category__category_id=categoryID)
    if not brand_name and not categoryID:
        products_images = all_products

    data = {}
    data['products_images'] = products_images
    data['categories'] = categories

    list_of_brands=[]
    for i in all_products:
        if i.product.brand not in list_of_brands:
            list_of_brands.append(i.product.brand)
    data['brand'] = list_of_brands


    return render(request, 'myShop/home.html', locals())


def index(request):
    latest_question_list = Product.objects.order_by('-product_id')[:10]
    context = {'latest_question_list': latest_question_list, }
    template = loader.get_template('myShop/index.html')
    return render(request, 'myShop/index.html', context)


def product(request, id):
    product = Product.objects.get(product_id=id)
    session_key = request.session.session_key
    categories_list = ProductCategory.objects.order_by('name')
    if not session_key:
        request.session.cycle_key()
    print(request.session.session_key)

    return render(request, 'myShop/product.html', locals())


def official(request):
    return render(request, 'myShop/official.html')


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = Basket.objects.filter(session_key=session_key, is_active=True).exclude(order__isnull=False)
    price_for_order = 0
    form = CheckoutBuyerForm(request.POST or None)
    for product in products_in_basket:
        price_for_order += product.total_price

    if request.POST:
        print(request.POST)
        if form.is_valid():
            print('Yes')
            data = request.POST
            name = data.get("name", 'user')
            last_name = data.get("last_name", ' ')
            number = data["number"]
            address = data.get("address", ' ')
            email = data['email']
            customer, created = Customers.objects.get_or_create(email=email,number=number, defaults={'name': name,
                                                                                       'last_name': last_name,
                                                                                       'address': address})
            order = Orders.objects.create(customer=customer,status_id=2,delivery_type='courier')
            for item,value in data.items():
                if item.startswith('number_in_basket_'):
                    products_in_basket_id=item.split('number_in_basket_')[1]
                    product = Basket.objects.get(id=products_in_basket_id)
                    product.count=value
                    product.order=order
                    product.save(force_update=True)

                    ProductInOrder.objects.create(product=product.product, count=product.count, price_per_item=product.price_per_item,
                                                  total_price=product.total_price, order=order)

                    print(id)
        else:
            print('No')

    return render(request, 'myShop/checkout.html', locals())

def basket(request):
    return_dict = {}
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    number = data.get("number")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        Basket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = Basket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                            is_active=True, order=None, defaults={"count": number})
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

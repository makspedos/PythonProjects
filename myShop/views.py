from django.shortcuts import render
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse


def home(request):
    categories = ProductCategory.objects.all()
    brand = Brand.objects.all()
    form = ProductFilterForm(request.GET)
    queryset = ProductImage.objects.filter(is_active=True, is_main=True)

    if form.is_valid():

        # apply filters based on user input
        name = form.cleaned_data.get('product_name')
        if name:
            queryset = queryset.filter(product__product_name__icontains=name)

        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(product__price__range=(min_price, max_price))
        if min_price:
            queryset = queryset.filter(product__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(product__price__lte=max_price)

        category = form.cleaned_data.get('category')
        print(category)
        if category:
            queryset = queryset.filter(product__category_id=category)

        brand = form.cleaned_data.get('brand')
        if brand:
            queryset = queryset.filter(product__brand_id=brand)

        size = form.cleaned_data.get('size')
        if size:
            queryset = queryset.filter(product__size=int(size))

    context = {
        'form': form,
        'products': queryset
    }

    all_products = ProductImage.objects.filter(is_active=True, is_main=True)
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')
    products_images = all_products

    data = {}
    data['products_images'] = products_images
    data['categories'] = categories
    data['brand'] = brand
    return render(request, 'myShop/home.html', locals())


def product(request, id):
    product = Product.objects.get(product_id=id)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    print(request.session.session_key)

    return render(request, 'myShop/product.html', locals())


def generate_pdf(request):
    # Get the last purchase information for the current user
    last_purchase = Orders.objects.last()

    products = ProductInOrder.objects.filter(order=last_purchase.order_id)

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="last_purchase.pdf"'

    # Create a canvas and add the last purchase information to it
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create data for the table
    data = [['Product', 'Brand', 'Count', 'Price']]
    for item in products:
        data.append([item.product.product_name, item.product.brand.brand_name, item.count, item.total_price])

    title_text = "Your order"
    title_style = getSampleStyleSheet()["Title"]
    title = Paragraph(title_text, title_style)

    # Create the table and set style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('RIGHTPADDING', (0, 0), (-1, -1), 50),
    ]))
    # Build the PDF document and save it to the response
    elements = [title, table]
    doc.build(elements)
    return response


def checkout(request):
    session_key = request.session.session_key
    pdf = False

    print(request.session.session_key)
    products_in_basket = Basket.objects.filter(session_key=session_key, is_shown=True).exclude(order__isnull=False)

    if len(products_in_basket) > 0:
        is_any_product = True
    else:
        is_any_product = False

    price_for_order = 0

    for product in products_in_basket:
        price_for_order += product.total_price

    form = CheckoutBuyerForm(request.POST or None)

    delivery_choices = form.fields['delivery_type'].choices
    payment_choices = form.fields['payment_type'].choices

    if request.POST:
        print(request.POST)
        if form.is_valid():
            pdf = True
            data = request.POST
            name = data.get("name", 'user')
            last_name = data.get("last_name", ' ')
            phone = data.get("phone", '')
            phone_regex = r'^\+380\d{9}$'
            if not re.match(phone_regex, phone):
                form.add_error('phone', 'Номер телефону має починатись на +380 і мати 12 цифр в загалом.')
                return render(request, 'myShop/checkout.html', locals())

            address = data.get("address", ' ')
            email = data['email']
            if Customers.objects.filter(email=email).exclude(phone=phone).exists() \
                    or Customers.objects.filter(phone=phone).exclude(email=email).exists():
                form.add_error('email', 'Почта та номер телефону вже використовувались у системі та не співпадають.')
                return render(request, 'myShop/checkout.html', locals())

            delivery_type = data['delivery_type']
            payment_type = data.get('payment_type', 'Cash')
            customer, created = Customers.objects.get_or_create(email=email,  defaults={'name': name,
                                                                                                    'last_name': last_name,
                                                                                                    'address': address,
                                                                                                    'phone' : phone,
                                                                                                    })
            order = Orders.objects.create(customer=customer, status_id=2, delivery_type=delivery_type,
                                          payment_type=payment_type  # total_price=price_for_order
                                          )
            for item, value in data.items():
                if item.startswith('number_in_basket_'):
                    products_in_basket_id = item.split('number_in_basket_')[1]
                    product = Basket.objects.get(id=products_in_basket_id)
                    product.count = value
                    product.order = order
                    product.save(force_update=True, is_shown=False)

                    ProductInOrder.objects.create(product=product.product, count=product.count,
                                                  price_per_item=product.price_per_item,
                                                  total_price=product.total_price, order=order)

            is_any_product = False
        else:
            print('Error')

    return render(request, 'myShop/checkout.html', locals())


def basket(request):
    session_key = request.session.session_key
    return_dict = {}
    data = request.POST
    product_id = data.get("product_id")
    number = data.get("number")
    is_delete = data.get("is_delete")
    product_in_basket = Basket.objects.filter(is_shown=True)
    if is_delete == 'true':
        Basket.objects.filter(id=product_id).update(is_shown=False)

    else:
        new_product, created = Basket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                            is_shown=True, order=None, defaults={"count": number})
        print(product_in_basket)
        if not created:
            print(product_in_basket)
            new_product.count += int(number)
            new_product.save(force_update=True)

    products_in_basket = Basket.objects.filter(session_key=session_key, is_shown=True, order__isnull=True)
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

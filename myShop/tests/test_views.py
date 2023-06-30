from django.test import TestCase, Client
from django.urls import reverse
from myShop.models import *
from myShop.forms import ProductFilterForm

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_list = reverse('myShop:home')
        self.url_products = reverse('myShop:product', args=[100])
        self.url_pdf = reverse("myShop:generate_pdf")
        self.url_home = reverse('myShop:home')
        Brand.objects.create(brand_name='Puma')
        Brand.objects.create(brand_name='Adidas')
        ProductCategory.objects.create(name='Взуття')
        MeasuredUnit.objects.create(measured_unit_id=55,name='cm')

        Product.objects.create(product_id = 100, size=2, amount=3, product_info='ssd',
                               price=200, product_name='sds', is_active=True,
                               brand= Brand.objects.get(brand_name='Puma'),
                               category= ProductCategory.objects.get(name='Взуття'),
                                measured_unit=MeasuredUnit.objects.get(measured_unit_id=55, name='cm'))

        Product.objects.create(product_id=101, size=2, amount=3, product_info='ssd',
                               price=50, product_name='sds2', is_active=True,
                               brand=Brand.objects.get(brand_name='Adidas'),
                               category=ProductCategory.objects.get(name='Взуття'),
                               measured_unit=MeasuredUnit.objects.get(measured_unit_id=55, name='cm'))



    def test_project_list_GET(self):
        response = self.client.get(self.url_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'myShop/home.html')

    def test_product_view(self):
        response = self.client.get(self.url_products)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'myShop/product.html')

    def test_pdf(self):
        Customers.objects.create(name='qwe', last_name='ewq', email='qweewqs@gmail.com', address='as23we',
                                 phone='+380912315522')
        Status.objects.create(status_name="Ready", is_active=True)
        Orders.objects.create(customer=Customers.objects.get(name="qwe"), total_price=300,
                              status=Status.objects.get(status_name='Ready'),
                              payment_type='Cash', delivery_type='Courier')
        ProductInOrder.objects.create(order=Orders.objects.get(total_price=300),
                                      product=Product.objects.get(product_id=100),
                                      count=50, price_per_item=100, total_price=300)
        response = self.client.get(self.url_pdf)
        self.assertEquals(response.status_code, 200)

    def test_home_get(self):
        ProductImage.objects.create(product=Product.objects.get(product_id=100),
                                    product_image='images/1',
                                    is_active=True,
                                    is_main=True,
                                    )
        ProductImage.objects.create(product=Product.objects.get(product_id=101),
                                    product_image='images/1',
                                    is_active=True,
                                    is_main=True,
                                    )
        a = ProductCategory.objects.get(name='Взуття')

        form_data = {
            'min_price': 51,
            'category': a.category_id,
        }

        response = self.client.get(self.url_home, form_data)

        result = response.context['queryset']

        product_test = ProductImage.objects.get(product_id=100)

        self.assertIn(product_test, result)
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'myShop/home.html')





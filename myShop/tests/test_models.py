from django.test import TestCase, Client
from django.urls import reverse
from myShop.models import *


class TestModels(TestCase):
    def setUp(self):
        self.brand_1 = Brand.objects.create(brand_name='Puma')
        self.brand_2 = Brand.objects.create(brand_name='Adidas')
        self.category = ProductCategory.objects.create(name='Взуття')
        self.measured = MeasuredUnit.objects.create(measured_unit_id=55, name='cm')

        self.product_1 = Product.objects.create(product_id=100, size=2, amount=3,
                                                product_info='ssd', price=200, product_name='sds',
                                                is_active=True, brand=self.brand_1, category=self.category,
                                                measured_unit=self.measured)

        self.product_2 = Product.objects.create(product_id=101, size=2, amount=3,
                                                product_info='ssd', price=50, product_name='sds2',
                                                is_active=True, brand=self.brand_1, category=self.category,
                                                measured_unit=self.measured)

        self.customer = Customers.objects.create(name='asd', last_name='eew', email='asdeeew@gmail.com',
                                                 address='as23we',
                                                 phone='+380912315522')

        self.status = Status.objects.create(status_name="Ready", is_active=True)
        self.order = Orders.objects.create(customer=self.customer, status=self.status, payment_type='Cash',
                                           delivery_type='Courier')

        self.product_in_order = ProductInOrder.objects.create(order=self.order, product=self.product_1, count=3)

    def test_product_in_order(self):
        print(f'price: {self.product_in_order.product.price}')
        self.assertEquals(self.product_in_order.total_price, 600)

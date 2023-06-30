from django.test import SimpleTestCase
from myShop.views import *
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):
    def test_program_all(self):
        url = reverse('myShop:home')
        self.assertEquals(resolve(url).func, home)

    def test_program_user(self):
        url = reverse('myShop:product', args=[1])
        self.assertEquals(resolve(url).func, product)
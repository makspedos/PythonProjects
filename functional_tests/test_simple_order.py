import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from .ancestor_test import AncestorTest

class TestOrder(AncestorTest):
    def __init__(self):
        super().__init__()
        self.form_dict = {
            'name': 'test_name',
            'last_name': 'test_last_name',
            'email': 'ds',
            'phone': '+380952114422',
            'address': 'wqeqw',
        }
        self.form_select_dict = {
            'payment_type': 'Готівка',
            'delivery_type': "Кур`єр"
        }

    def template_method(self,amount):
        self.select_product()
        self.add_product(amount)
        self.make_order()

    def form_test(self):
        for key, value in self.form_dict.items():
            a = self.find_element_by_name(key)
            a.send_keys(value)
        for key, value in self.form_select_dict.items():
            result = Select(self.find_element_by_name(key))
            result.select_by_visible_text(value)

    def select_product(self):
        product_link = self.driver.find_elements('xpath',
                                            '//div[contains(@class, "product-item")][.//h5[text()[contains(., "Nike")]]]//a')
        for link in product_link:
            if link.get_attribute('href'):
                link.click()
                break
        self.wait()

    def add_product(self, amount):
        add_product_amount = self.find_element_by_id('num')
        add_product_amount.send_keys(amount)

        self.click_element_by_xpath('//button[@class="btn btn-success btn-buy"][@id="submit-btn"]')

        basket_link = self.driver.find_element('xpath',
                                          '//li[contains(@class,"nav-item")][.//a[text()[contains(., "Переглянути")]]]//a')
        basket_link.get_attribute('href')
        basket_link.click()

        self.wait()


    def make_order(self):
        self.form_test()
        self.click_element_by_xpath('//button[@class="btn btn-primary btn-lg"]')


test = TestOrder()

test.template_method(amount=3)
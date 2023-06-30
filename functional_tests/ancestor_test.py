import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from abc import abstractmethod, ABC


class AncestorTest(ABC):
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.maximize_window()
        self.driver.get('http://127.0.0.1:8000/home')


    @abstractmethod
    def template_method(self, amount):
        pass

    def wait(self):
        time.sleep(1)

    def find_element_by_name(self, name):
        return self.driver.find_element(By.NAME, name)

    def find_element_by_id(self, id):
        return self.driver.find_element(By.ID, id)

    def click_element_by_xpath(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()




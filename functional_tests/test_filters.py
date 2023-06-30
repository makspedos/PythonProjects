from functional_tests.ancestor_test import AncestorTest


class TestFilters(AncestorTest):
    def __init__(self):
        super().__init__()
        self.filters_radio = {
            "category":"Взуття",
            'brand': "Puma",
        }
        self.filters_text = {
            'min_price': 50,
            'max_price': 1900,
        }

    def template_method(self, amount):
        pass

    def make_filter(self):
        self.wait()
        for key, value in self.filters_radio.items():
            self.click_element_by_xpath(f'//label[contains(., "{value}")][.//input[@name="{key}"]]')

        for key, value in self.filters_text.items():
            element = self.find_element_by_name(key)
            element.send_keys(value)
        self.click_element_by_xpath('//button[@type="submit"]')

test = TestFilters()

test.make_filter()
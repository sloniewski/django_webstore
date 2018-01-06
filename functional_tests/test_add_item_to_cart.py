from .base import FunctionalTest

from product.models import Product

from selenium.webdriver.support.ui import WebDriverWait


class AddItemToCartTest(FunctionalTest):

    def test_add_item_to_cart(self):
        product = Product.objects.create(name='my-test-product')
        self.browser.get('http://localhost:8000/product/{}/'.format(product.slug))

        button = self.browser.find_element_by_id('add-to-cart')
        quantity_box = self.browser.find_element_by_id('item-quantity')

        quantity_box.send_keys('2')
        button.click()
        element = WebDriverWait(
                driver=self.browser,
                timeout=2,
                poll_frequency=0.5
            ).until(
                    method=lambda x: x.find_element_by_id('cart-item-count').text == '2',
                    message='Item not added to car in 2 sec time'
                )

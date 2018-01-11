from .base import FunctionalTest

from product.models import Product

from selenium.webdriver.support.ui import WebDriverWait
import time


class AddItemToCartTest(FunctionalTest):

    def test_add_item_to_cart(self):
        product = Product.objects.create(name='just for testing')
        url = '{}/product/{}/'.format(
            self.live_server_url,
            product.slug,
            )

        self.browser.get(url)
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

        button.click()
        element = WebDriverWait(
                driver=self.browser,
                timeout=2,
                poll_frequency=0.5
            ).until(
                    method=lambda x: x.find_element_by_id('cart-item-count').text == '4',
                    message='Item not added to car in 2 sec time'
                )

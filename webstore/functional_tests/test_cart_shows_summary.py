from webstore.cart.models import Cart

from .base import FunctionalTest


class TestCartShowsSummary(FunctionalTest):

    def test_cart_shows_summary(self):
        self.session.create()
        cart = Cart.objects.get_or_create(session_id=self.session.session_key)[0]
        prod_a = self.create_test_product(price=4.12)
        prod_b = self.create_test_product(price=2.15)

        cart.add_item(item=prod_a.id, qty=2)
        cart.add_item(item=prod_b.id, qty=5)

        url = self.live_server_url + '/cart/'
        self.browser.get(url)

        self.browser.add_cookie({
            'name': 'sessionid',
            'value': self.session.session_key,
            'path': '/',
        })

        self.browser.refresh()

        cart_items_list = self.browser.find_elements_by_class_name('cart-list-item')
        self.assertIn(prod_a.name, cart_items_list)
        self.assertIn(prod_b.name, cart_items_list)

        cart_summary = self.browser.find_element_by_id('cart-summary')
        self.assertEqual(cart_summary.text, '18.99')

from django.contrib import messages
from django.utils.translation import gettext as _

from products.models import Product


class Cart:

    def __init__(self, request):
        """
        Initialize a new cart for the user making the request. If no user is provided 
        """

        self.request = request
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        Add a product to the cart or update its quantity
        """

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, _('Product Successfully added to Your Cart.'))
        self.save()

    def save(self):
        """
        Mark the session as "modified" to make sure it gets saved
        """

        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        """

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

            messages.warning(self.request, _('Product Successfully removed from Your Cart.'))
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """

        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session
        """

        del self.session['cart']
        self.save()

    def get_total_price(self):
        """
        Get the total price of all items in the cart
        """
        product_ids = self.cart.keys()
        
        return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
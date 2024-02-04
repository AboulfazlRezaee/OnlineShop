from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(_("Is Paid"), default=False)

    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=80)
    phone = models.CharField(_("Phone Number"), max_length=12)
    address = models.CharField(_("Address"), max_length=700)
    zipcode = models.CharField(_("Zipcode"), max_length=10)
    order_note = models.CharField(_("Order Note"), max_length=500, blank=True)

    datetime_created = models.DateTimeField(_('Date-Time of'), auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name= "order_item", verbose_name=_("products"))
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    price = models.PositiveIntegerField(_("Price"))

    def __str__(self):
        return f'Order Item {self.id}: {self.product} x {self.quantity} (price: {self.price})'


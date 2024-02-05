from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext as _

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm

# Create your views here.

def cart_detail_view(request):
    cart = Cart(request)
    context = {'cart': cart}

    for item in cart:
        item['update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
              'inplace': True,
              })

    return render(request, 'cart/cart_detail.html', context)

@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddToCartProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])


    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)


    return redirect('cart:cart_detail')

@require_POST
def clear_cart(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('You Cannot Clear An Empty Cart.'))
    else:
        messages.success(request, _('Your Cart Successfully Cleared.'))
        cart.clear()

    return redirect('product_list')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm

# Create your views here.

def cart_detail_view(request):
    cart = Cart(request)
    context = {'cart': cart}

    return render(request, 'cart/cart_detail.html', context)

def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddToCartProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity)

    messages.success(request, 'کالا با موفقیت در سبد خرید شما اضافه شد.')

    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    messages.warning(request, 'کالا با موفقیت از سبد خرید شما حذف شد.')

    return redirect('cart:cart_detail')
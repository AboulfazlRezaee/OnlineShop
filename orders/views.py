from django.shortcuts import render

# Create your views here.

def order_create_view(request):
    return render(request, 'orders/order_create.html')
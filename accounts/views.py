# from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.


def account_detail(request):
    return render(request, 'accounts/account_detail.html')
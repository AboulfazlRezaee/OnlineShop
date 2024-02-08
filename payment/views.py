import requests
import json

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse

from django.conf import settings

from orders.models import Order

# Create your views here.

def payment_process(request):
    
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,  # required
        'amount': rial_total_price,  # required
        'description': f'#{order.id} : {order.user.first_name} {order.user.last_name}', # required
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),  # required
    }

    request_j = json.dumps(request_data)
    res = requests.post(url=zarinpal_request_url, data=request_j, headers=request_header)

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error From Zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':

        request_header = {
        "accept": "application/json",
        "content-type": "application/json",
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,  # required
            'amount': rial_total_price,  # required
            'authority': payment_authority,  # required
        }

        res = requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
        )

        if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse("پرداخت با موفقیت انجام شد")
            
            elif payment_code == 101:
                return HttpResponse("پرداخت قبلا انجام شده است.")
            
            else:
                return HttpResponse("پرداخت انجام نشد")
            
    else:
        return HttpResponse("پرداخت انجام نشد")






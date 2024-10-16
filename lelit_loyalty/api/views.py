from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest
import json
from . import models


def index(request):
    try:
        req = json.loads(request.body)
        if req['jsonrpc'] == '2.0':
            data = {
                'jsonrpc': '2.0',
                'id': req['id'],
            }
            if request.META['HTTP_AUTHORIZATION'] != 'HTcA3EMBx9ViZIrimXhR2SgIHht4Hb':
                data['error'] = ERRORS[1002]
                return JsonResponse(data)
            match req['method']:
                case 'GetClientDetail':
                    try:
                        user = models.User.objects.get(barcode=req['params']['barcode'])
                        data['result'] = {
                            'name': user.name,
                            'phone': user.phone,
                            'barcode': user.barcode,
                            'birth_date': user.birth_date,
                            'city': user.city,
                            'balance': user.balance
                        }
                        return JsonResponse(data=data)
                    except ObjectDoesNotExist:
                        data['error'] = ERRORS[1003]
                        return JsonResponse(data)
                case 'NewPurchase':
                    try:
                        types = ['cash', 'card', 'bonus']
                        if req['params']['type'] not in types:
                            data['error'] = ERRORS[1004]
                            return JsonResponse(data)
                        user = models.User.objects.get(barcode=req['params']['barcode'])
                        if req['params']['type'] == 'bonus':
                            if int(req['params']['total_sum'] / 100) > user.balance:
                                data['error'] = ERRORS[1005]
                                return JsonResponse(data)
                            else:
                                user.balance -= int(req['params']['total_sum'] / 100)
                                user.save()
                        else:
                            user.balance += int(req['params']['total_sum'] / 10000)
                            user.save()
                        purchase = models.Purchase(
                            user=user,
                            sum=req['params']['total_sum'],
                            type=req['params']['type'],
                            datetime=req['params']['datetime'],
                        )
                        purchase.save()
                        data['result'] = 'Success'
                        return JsonResponse(data)
                    except ObjectDoesNotExist:
                        data['error'] = ERRORS[1003]
                        return JsonResponse(data)
                case _:
                    data['error'] = ERRORS[1001]
                    return JsonResponse(data)

        else:
            return HttpResponseBadRequest('Invalid JSON')
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest('Invalid JSON')


ERRORS = {
    1001: {
        'code': 1001,
        'message': 'Wrong Method'
    },
    1002: {
        'code': 1002,
        'message': 'Wrong Auth'
    },
    1003: {
        'code': 1003,
        'message': 'Client does not exist'
    },
    1004: {
        'code': 1004,
        'message': 'Wrong payment type'
    },
    1005: {
        'code': 1005,
        'message': 'Not enough bonus'
    }
}
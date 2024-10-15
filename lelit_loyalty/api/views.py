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
            if request.META['HTTP_AUTHORIZATION'] == '12345':
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
                            user = models.User.objects.get(barcode=req['params']['barcode'])

                            data['result'] = 'Success'
                            return JsonResponse(data)
                        except ObjectDoesNotExist:
                            data['error'] = ERRORS[1003]
                            return JsonResponse(data)
                    case _:
                        data['error'] = ERRORS[1001]
                        return JsonResponse(data)
            else:
                data['error'] = ERRORS[1002]
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
    }
}
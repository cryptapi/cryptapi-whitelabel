from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from settings.utils import get as get_setting
from settings.models import Currency

from .utils import validate_addresses, generate_nonce, build_callback_url, process_request, send_callback, fetch_logs
from .models import Request

from pprint import pformat
from decimal import Decimal

import json


def create(_r, coin):

    currency = Currency.get(ticker=coin)

    if not currency:
        return JsonResponse({'status': 'error', 'error': 'Currency not found'})

    _callback = _r.GET.get('callback')
    address = _r.GET.get('address')
    notify_pending = bool(_r.GET.get('pending', False))
    notify_post = bool(_r.GET.get('post', False))
    notify_confirmations = min(1000000000, int(_r.GET.get('confirmations', 1)))
    priority_slug = _r.GET.get('priority', 'default')

    extra_fee = get_setting('extra_fee')

    address_out, address_dict = validate_addresses(address, extra_fee, currency.coldwallet)

    if not address_out or not _callback:
        return JsonResponse({'status': 'error', 'error': 'You must provide a valid address and a callback URL'}, status=400)

    try:
        validator = URLValidator()
        validator(_callback)
    except ValidationError:
        return JsonResponse({'status': 'error', 'error': 'Callback URL malformed, please provide a correct URL'}, status=400)

    nonce = generate_nonce()

    _request, created = Request.objects.get_or_create(callback_url=_callback, coin=currency)

    if created:
        _request.address_out = pformat(address_dict)
        _request.raw_address_out = address
        _request.notify_pending = notify_pending
        _request.notify_post = notify_post
        _request.notify_confirmations = notify_confirmations
        _request.priority_slug = priority_slug
        _request.extra_fee = extra_fee
        _request.nonce = nonce

        _request.save()

    callback_params = {
        'request_id': _request.id,
        'nonce': _request.nonce,
    }

    params = {
        'address': address_out,
        'callback': build_callback_url(_r, callback_params),
        'token': get_setting('affiliate_token'),
        'pending': int(notify_pending),
        'post': int(notify_post),
        'confirmations': notify_confirmations,
        'priority': priority_slug,
    }

    raw_response = process_request(
        coin=currency.ticker,
        endpoint='create',
        params=params,
    )

    if raw_response.status_code == 200:

        _request.requestlog_set.create(
            raw_data=raw_response.text
        )

        response = raw_response.json()

        if response['status'] != 'success':
            return JsonResponse({'status': 'error', 'error': 'There was an error processing your request, please try again later'})

        if response['address_in'] != _request.address_in:
            _request.address_in = response['address_in']
            _request.save()

        if 'callback_url' in response:
            response['callback_url'] = _request.callback_url

        if 'address_out' in response:
            response['address_out'] = _request.raw_address_out

        return JsonResponse(response)

    return JsonResponse({'status': 'error', 'error': 'There was an error processing your request, please try again later'})


def logs(_r, coin):
    currency = Currency.get(ticker=coin)

    if not currency:
        return JsonResponse({'status': 'error', 'error': 'Currency not found'})

    try:
        _callback = _r.GET.get('callback')

        try:
            _req = Request.objects.get(callback_url=_callback)

            callback_params = {
                'request_id': _req.id,
                'nonce': _req.nonce,
            }

            callback_url = build_callback_url(_r, callback_params)

            _logs = fetch_logs(currency.ticker, callback_url)

            if _logs:

                if 'callback_url' in _logs:
                    _logs['callback_url'] = _req.callback_url

                if 'address_out' in _logs:
                    _logs['address_out'] = _req.raw_address_out

                if 'callbacks' in _logs:
                    for c in _logs['callbacks']:
                        c.pop('logs', None)

                        if _req.extra_fee > 0:
                            c['fee_percent'] = Decimal(c['fee_percent']) + _req.extra_fee
                            c['fee'] = int(c['fee']) + (int((int(c['value']) - int(c['fee'])) * (_req.extra_fee / 100)))

                return JsonResponse(_logs)

        except Request.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': "Callback not found"}, status=404)

    except Exception:
        pass

    return JsonResponse({'status': 'error', 'error': "Your request couldn't be processed, please try again later"}, status=400)


def callback(_r, request_id, nonce):
    try:
        _req = Request.objects.get(id=request_id)

        if nonce == _req.nonce:
            params = _r.GET.dict()
            params['address_out'] = _req.raw_address_out

            if _req.extra_fee > 0 and 'value_forwarded' in params:
                params['value_forwarded'] = int(int(params['value_forwarded']) * (Decimal('1.0') - (_req.extra_fee / 100)))
                params['value_forwarded_coin'] = str(Decimal(params['value_forwarded_coin']) * (Decimal('1.0') - (_req.extra_fee / 100)))

            _payment, created = _req.payment_set.get_or_create(txid_in=params['txid_in'])
            _payment.value_paid = params['value']
            _payment.confirmations = params['confirmations']
            _payment.pending = bool(int(params.get('pending', 0)))

            if 'value_forwarded' in params:
                _payment.value_received = params['value_forwarded']

            if 'txid_out' in params:
                _payment.txid_out = params['txid_out']

            _payment.save()

            _payment.paymentlog_set.create(
                raw_data=json.dumps(_r.GET)
            )

            if not _req.notify_pending and _payment.pending:
                return HttpResponse('*ok*')

            response = send_callback(_req, params)
            return HttpResponse(response)

    except Request.DoesNotExist:
        pass

    return HttpResponse('*ok*')



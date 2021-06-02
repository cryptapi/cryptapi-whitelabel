from django.shortcuts import reverse
from django.conf import settings
from urllib.parse import urlencode
from decimal import Decimal
import string
import random
import requests


def build_query_string(data):
    return urlencode(data)


def build_callback_url(_r, params):
    _url = _r.build_absolute_uri(reverse('proxy:callback', kwargs=params))
    base_request = requests.Request(url=_url).prepare()
    return base_request.url


def fetch_logs(coin, callback_url):
    response = process_request(coin=coin, endpoint='logs', params={'callback': callback_url})

    if response.status_code == 200:
        return response.json()

    return None


def process_request(coin, endpoint='create', params=None):
    response = requests.get(
        url="{base_url}{coin}/{endpoint}".format(
            base_url=settings.CRYPTAPI_URL,
            coin=coin.replace('_', '/'),
            endpoint=endpoint,
        ),
        params=params
    )

    return response


def send_callback(req, params):

    if not req.notify_post:
        response = requests.get(req.callback_url, params=params)
    else:
        response = requests.post(req.callback_url, data=params)

    return response.text.strip()


def process_addresses(address_str):

    try:
        payment_list = str(address_str).split('|')
        filtered_list = [x.split('@') for x in payment_list if x]

        if len(filtered_list) == 1 and len(filtered_list[0]) == 1:
            return {filtered_list[0][0]: Decimal('1.0')}

        addr_dict = {addr: round(Decimal(pct), 2) for pct, addr in filtered_list if pct and addr}
        total = sum(addr_dict.values())

        if total == Decimal('1.0'):
            return addr_dict

    except Exception:
        pass

    return None


def validate_addresses(address_str, extra_fee, cold_wallet):

    addr_dict = process_addresses(address_str)

    if not addr_dict:
        return None

    if extra_fee and cold_wallet:
        remaining = Decimal('1.0') - (extra_fee / 100)
        addr_dict = {addr: round(pct * remaining, 4) for addr, pct in addr_dict.items()}

        total = sum(addr_dict.values())

        addr_dict[cold_wallet] = Decimal('1.0') - total

    if len(addr_dict) == 1:
        return list(addr_dict.keys())[0], addr_dict

    return '|'.join(['{pct}@{addr}'.format(addr=addr, pct=pct) for addr, pct in addr_dict.items()]), addr_dict


def generate_nonce(length=32):

    # Not cryptographically secure, but good enough for generating nonces

    sequence = string.ascii_letters + string.digits

    return ''.join([random.choice(sequence) for i in range(length)])

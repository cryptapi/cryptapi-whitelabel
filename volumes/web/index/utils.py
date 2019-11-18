from settings.utils import get as get_setting


def get_fees():

    multiplier = 1 if not get_setting('extra_fee') else 2

    fees = {
        'btc': {
            'min_tx': get_setting('btc_minimum_transfer') * multiplier,
            'min_fee': get_setting('btc_minimum_fee'),
            'fee': get_setting('btc_fee') + get_setting('extra_fee'),
        },
        'bch': {
            'min_tx': get_setting('bch_minimum_transfer') * multiplier,
            'min_fee': get_setting('bch_minimum_fee'),
            'fee': get_setting('bch_fee') + get_setting('extra_fee'),
        },
        'ltc': {
            'min_tx': get_setting('ltc_minimum_transfer') * multiplier,
            'min_fee': get_setting('ltc_minimum_fee'),
            'fee': get_setting('ltc_fee') + get_setting('extra_fee'),
        },
        'eth': {
            'min_tx': get_setting('eth_minimum_transfer') * multiplier,
            'min_fee': get_setting('eth_minimum_fee'),
            'fee': get_setting('eth_fee') + get_setting('extra_fee'),
        },
        'xmr': {
            'min_tx': get_setting('xmr_minimum_transfer') * multiplier,
            'min_fee': get_setting('xmr_minimum_fee'),
            'fee': get_setting('xmr_fee') + get_setting('extra_fee'),
        },
        'iota': {
            'min_tx': get_setting('iota_minimum_transfer') * multiplier,
            'min_fee': get_setting('iota_minimum_fee'),
            'fee': get_setting('iota_fee') + get_setting('extra_fee'),
        },
    }

    for coin, values in fees.items():
        for k, v in values.items():
            values[k] = format(v.normalize(), 'f')

    return fees

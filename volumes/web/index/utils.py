from settings.utils import get as get_setting
from settings.models import Currency


def get_fees():

    multiplier = 1 if not get_setting('extra_fee') else 2

    fees = {c.ticker: {
        'name': c.name,
        'ticker': c.ticker,
        'min_tx': c.minimum_transfer * multiplier,
        'min_fee': c.minimum_fee,
        'fee': c.fee + get_setting('extra_fee')
    } for c in Currency.list()}

    for coin, values in fees.items():
        values['min_fee'] += (get_setting('extra_fee') / 100) * values['min_tx']

        for k, v in values.items():
            values[k] = format(v.normalize(), 'f')

    return fees

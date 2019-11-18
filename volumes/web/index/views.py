from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils import get_fees


def index(_r):
    return render(_r, 'index/index.html')


def docs(_r):
    return render(_r, 'index/docs.html')


def docs_api_json(_r):
    data = render_to_string('index/api.json', context=get_fees(), request=_r)
    return HttpResponse(data, content_type='application/json')


def get_started(_r):
    _c = {'site_description': 'Get Started'}

    return render(_r, 'index/get_started.html', _c)


def pricing(_r):
    _c = {
        'site_description': 'Pricing / Fees',
        **get_fees(),
    }

    return render(_r, 'index/pricing.html', _c)


def go_home(_r, exception=None, template_name=None):
    return redirect('index:index')

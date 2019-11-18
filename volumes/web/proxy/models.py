from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Request(models.Model):
    coin = models.CharField(_('Coin'), max_length=16, choices=settings.COINS)
    address_in = models.CharField(_('Payment Address'), max_length=255, default='', db_index=True)
    address_out = models.CharField(_('Receiving Addresses'), max_length=2048, default='')
    raw_address_out = models.CharField(_('Raw Receiving Addresses'), max_length=2048, default='')
    extra_fee = models.DecimalField(_('Extra Fee'), default=0, max_digits=3, decimal_places=2)
    callback_url = models.CharField(_('Callback URL'), max_length=2048, default='')
    notify_pending = models.BooleanField(_('Notify Pending'), default=False)

    nonce = models.CharField(_('Nonce'), max_length=32, default='')
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    last_update = models.DateTimeField(_('Last Update'), auto_now=True)

    def __str__(self):
        return "#{} {} ({}, {})".format(self.id, self.address_in, self.get_coin_display(), self.timestamp.strftime('%x %X'))


class Payment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    value_paid = models.DecimalField(_('Value Paid'), default=0, max_digits=65, decimal_places=0)
    value_received = models.DecimalField(_('Value Received'), default=0, max_digits=65, decimal_places=0)
    txid_in = models.CharField(_('TXID in'), max_length=256, default='')
    txid_out = models.CharField(_('TXID out'), max_length=256, default='')
    pending = models.BooleanField(default=True)
    confirmations = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{}, {}, {} ({})".format(self.request.id, self.value_paid, self.request.get_coin_display(), self.timestamp.strftime('%x %X'))


class RequestLog(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    raw_data = models.CharField(max_length=8192)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{} ({})".format(self.request_id, self.timestamp.strftime('%x %X'))


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    raw_data = models.CharField(max_length=8192)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{} ({})".format(self.payment_id, self.timestamp.strftime('%x %X'))

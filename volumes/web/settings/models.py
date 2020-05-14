from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(_('Name'), max_length=64)
    ticker = models.CharField(_('Ticker'), max_length=16, unique=True, db_index=True)
    coldwallet = models.CharField(_('Cold Wallet'), max_length=255, default='')
    active = models.BooleanField(_('Active'), default=True)

    # CryptAPI configs
    fee = models.DecimalField(_('Fee'), default=1.0, max_digits=3, decimal_places=2)
    minimum_transfer = models.DecimalField(_('Min. Transfer'), default=0.0002, max_digits=10, decimal_places=8)
    minimum_fee = models.DecimalField(_('Min. Fee'), default=0.00002, max_digits=10, decimal_places=8)

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, ticker):
        try:
            return cls.objects.get(ticker__iexact=ticker.replace('/', '_'), active=True)

        except cls.DoesNotExist:
            pass

        return None

    @classmethod
    def list(cls):
        return cls.objects.filter(active=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Settings(models.Model):
    site_active = models.BooleanField(_('Site Active'), default=True)
    site_title = models.CharField(_('Site Title'), max_length=255, default='White Label')
    site_url = models.CharField(_('Site URL'), max_length=255, default='https://example.io')
    contact_email = models.EmailField(_('Contact Email'), max_length=255, default='admin@example.io')

    affiliate_token = models.CharField(_('Affiliate Token (Optional: Send an email to info@cryptapi.io to request yours)'), max_length=128, default='', blank=True)
    extra_fee = models.DecimalField(_('Extra Fee'), default=0, max_digits=3, decimal_places=2)

    def __str__(self):
        return self.site_title

    class Meta:
        verbose_name = verbose_name_plural = 'Settings'

from django.db import models
from django.utils.translation import gettext_lazy as _


class Settings(models.Model):
    site_active = models.BooleanField(_('Site Active'), default=True)
    site_title = models.CharField(_('Site Title'), max_length=255, default='White Label')
    site_url = models.CharField(_('Site URL'), max_length=255, default='https://example.io')
    contact_email = models.EmailField(_('Contact Email'), max_length=255, default='admin@example.io')

    affiliate_token = models.CharField(_('Affiliate Token (Optional: Send an email to info@cryptapi.io to request yours)'), max_length=128, default='', blank=True)
    extra_fee = models.DecimalField(_('Extra Fee'), default=0, max_digits=3, decimal_places=2)

    btc_coldwallet = models.CharField(_('BTC Cold Wallet'), max_length=255, default='')
    bch_coldwallet = models.CharField(_('BCH Cold Wallet'), max_length=255, default='')
    ltc_coldwallet = models.CharField(_('LTC Cold Wallet'), max_length=255, default='')
    eth_coldwallet = models.CharField(_('ETH Cold Wallet'), max_length=255, default='')
    xmr_coldwallet = models.CharField(_('XMR Cold Wallet'), max_length=255, default='')
    iota_coldwallet = models.CharField(_('IOTA Cold Wallet'), max_length=255, default='')

    # CryptAPI configs
    btc_fee = models.DecimalField(_('BTC Fee'), default=1.0, max_digits=3, decimal_places=2)
    bch_fee = models.DecimalField(_('BCH Fee'), default=1.0, max_digits=3, decimal_places=2)
    ltc_fee = models.DecimalField(_('LTC Fee'), default=1.0, max_digits=3, decimal_places=2)
    eth_fee = models.DecimalField(_('ETH Fee'), default=1.0, max_digits=3, decimal_places=2)
    xmr_fee = models.DecimalField(_('XMR Fee'), default=1.0, max_digits=3, decimal_places=2)
    iota_fee = models.DecimalField(_('IOTA Fee'), default=1.0, max_digits=3, decimal_places=2)

    btc_minimum_transfer = models.DecimalField(_('BTC Min. Transfer'), default=0.0002, max_digits=10, decimal_places=8)
    bch_minimum_transfer = models.DecimalField(_('BCH Min. Transfer'), default=0.0005, max_digits=10, decimal_places=8)
    ltc_minimum_transfer = models.DecimalField(_('LTC Min. Transfer'), default=0.002, max_digits=10, decimal_places=8)
    eth_minimum_transfer = models.DecimalField(_('ETH Min. Transfer'), default=0.001, max_digits=10, decimal_places=8)
    xmr_minimum_transfer = models.DecimalField(_('XMR Min. Transfer'), default=0.0025, max_digits=10, decimal_places=8)
    iota_minimum_transfer = models.DecimalField(_('IOTA Min. Transfer'), default=0.05, max_digits=10, decimal_places=8)

    btc_minimum_fee = models.DecimalField(_('BTC Min. Fee'), default=0.00002, max_digits=10, decimal_places=8)
    bch_minimum_fee = models.DecimalField(_('BCH Min. Fee'), default=0.0002, max_digits=10, decimal_places=8)
    ltc_minimum_fee = models.DecimalField(_('LTC Min. Fee'), default=0.0008, max_digits=10, decimal_places=8)
    eth_minimum_fee = models.DecimalField(_('ETH Min. Fee'), default=0.0003, max_digits=10, decimal_places=8)
    xmr_minimum_fee = models.DecimalField(_('XMR Min. Fee'), default=0.0005, max_digits=10, decimal_places=8)
    iota_minimum_fee = models.DecimalField(_('IOTA Min. Fee'), default=0.025, max_digits=10, decimal_places=8)

    def __str__(self):
        return self.site_title

    class Meta:
        verbose_name = verbose_name_plural = 'Settings'

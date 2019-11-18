from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import Settings


class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('White Label'), {
           'fields': ('site_active', 'site_title', 'site_url', 'contact_email')
        }),
        (_('Fees'), {
            'fields': ('affiliate_token', 'extra_fee'),
            'description': "NOTE: extra fee will be added to the affiliate's reward, if you don't have an affiliate token and you set extra fee to 0, you will not receive anything"
        }),
        (_('Coins'), {
            'fields': (
                'btc_coldwallet',
                'bch_coldwallet',
                'ltc_coldwallet',
                'eth_coldwallet',
                'xmr_coldwallet',
                'iota_coldwallet',
            ),
            'description': "NOTE: if you have an affiliate token, these cold wallet addresses can't be the same as the affiliate address"
        }),
        (_('CryptAPI Settings'), {
            'fields': (
                ('btc_fee', 'btc_minimum_transfer', 'btc_minimum_fee'),
                ('bch_fee', 'bch_minimum_transfer', 'bch_minimum_fee'),
                ('ltc_fee', 'ltc_minimum_transfer', 'ltc_minimum_fee'),
                ('eth_fee', 'eth_minimum_transfer', 'eth_minimum_fee'),
                ('xmr_fee', 'xmr_minimum_transfer', 'xmr_minimum_fee'),
                ('iota_fee', 'iota_minimum_transfer', 'iota_minimum_fee'),
            ),
            'description': 'These are for display only and should reflect the real values on https://cryptapi.io/pricing/, otherwise your customers might complain of inaccuracies'
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Settings, SettingsAdmin)

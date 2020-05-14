from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import Settings, Currency


class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Base Config'), {
            'fields': (
                'name',
                'ticker',
                'coldwallet',
                'active',
            ),
            'description': "NOTE: extra fee will be added to the affiliate's reward, if you don't have an affiliate token and you set extra fee to 0, you will not receive anything"
        }),
        (_('CryptAPI Config'), {
            'fields': (
                'fee',
                'minimum_fee',
                'minimum_transfer',
            ),
            'description': 'These are for display only and should reflect the real values on https://cryptapi.io/pricing/, otherwise your customers might complain of inaccuracies'
        })
    )

    def has_delete_permission(self, request, obj=None):
        return False


class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('White Label'), {
           'fields': ('site_active', 'site_title', 'site_url', 'contact_email')
        }),
        (_('Fees'), {
            'fields': ('affiliate_token', 'extra_fee'),
            'description': "NOTE: extra fee will be added to the affiliate's reward, if you don't have an affiliate token and you set extra fee to 0, you will not receive anything"
        })
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Currency, CurrencyAdmin)

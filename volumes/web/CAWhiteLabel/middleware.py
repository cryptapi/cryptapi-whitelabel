from django.shortcuts import render
from django.http import JsonResponse


class SettingsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if 'admin' not in request.path:

            from settings.utils import get as get_setting
            settings = get_setting()

            if settings:
                request.settings = settings

                if not settings.site_active:
                    if not request.user.is_superuser:
                        if request.is_ajax():
                            return JsonResponse({'status': 'error', 'error': 'Website down for maintenance, please check back in a few minutes'}, status=503)
                        return render(request, 'disabled.html', status=503)

        return self.get_response(request)

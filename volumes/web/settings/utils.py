from django.core.exceptions import ImproperlyConfigured
from django.db import ProgrammingError


def get(key=None, default=None):

    from .models import Settings

    try:
        _settings = Settings.objects.get(id=1)

        if key:
            return getattr(_settings, key, default)
        return _settings

    except Settings.DoesNotExist:
        raise ImproperlyConfigured("Couldn't find suitable website settings")

    except ProgrammingError:
        pass

    return default


def set(key, value):

    from .models import Settings

    try:
        _settings = Settings.objects.get(id=1)
        setattr(_settings, key, value)
        _settings.save()

    except Settings.DoesNotExist:
        raise ImproperlyConfigured("Couldn't find suitable website settings")

def static_url(request):
    from django.conf import settings
    return {'STATIC_URL': settings.STATIC_URL}


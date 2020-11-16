from django.conf import settings

def revision_number_processor(request):
    return {'revision': settings.JAVASCRIPT_VERSION}

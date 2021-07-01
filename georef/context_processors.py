from django.conf import settings

def revision_number_processor(request):
    return {'revision': settings.JAVASCRIPT_VERSION}

def version_number_processor(request):
    version_string = '.'.join((settings.MAJOR, settings.MINOR, settings.PATCH))
    return {'version': version_string}

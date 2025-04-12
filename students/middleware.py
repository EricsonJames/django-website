from django.utils.translation import activate

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('lang')
        if lang:
            activate(lang)
            request.session['django_language'] = lang
        return self.get_response(request)

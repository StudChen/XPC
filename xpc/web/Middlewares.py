from django.http import HttpResponseRedirect

from web.models import Composer

need_login = ['/list/2/', '/comment']


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        cid = request.COOKIES.get('cid')
        composer = Composer.objects.filter(cid=cid).first()
        request.composer = composer
        if request.path in need_login:
            if not cid or composer:
                return HttpResponseRedirect('/login')
        response = self.get_response(request)
        self.process_response(request, response)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass
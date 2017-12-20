from django.http import HttpResponsePermanentRedirect
import random


class LocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        full_path = request.get_full_path()
        url = full_path.split('?')
        clear_url = url[0]

        page = request.GET.get('page', '')
        if '?page=' + page in full_path:
            return HttpResponsePermanentRedirect(
                clear_url + 'page-' + page + '/'
            )
        user_id = request.session.get('user_id', False)

        if not user_id:
            request.session['user_id'] = random.randint(1000, 9999)

    def process_response(self, request, response):
        # assert False, request.session['user_id']
        return response

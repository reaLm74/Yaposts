import logging

# from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


# class FilterIPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         allowed_ip = ['127.0.0.1']
#         ip = request.META.get('REMOTE_ADDR')
#         if ip not in allowed_ip:
#             raise PermissionDenied
#         response = self.get_response(request)
#         return response


class LoggingIP:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.META.get('REMOTE_ADDR')
        logger.info(f'Log in from IP {url}')
        response = self.get_response(request)
        return response

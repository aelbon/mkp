from django.db import connection
from .util.log_util import log_session_info
from .util.context_data_util import get_current_site_and_shop
from django.contrib.sites.models import Site
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
class DatabaseUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response      
        # Update ALLOWED_HOSTS from database
        hosts = Site.objects.values_list('domain', flat=True)
        settings.ALLOWED_HOSTS.extend(list(hosts))
        settings.CSRF_TRUSTED_ORIGINS = [f'http://{host}:3333' for host in  settings.ALLOWED_HOSTS]
        # Middleware won't be used after initialization
        # raise MiddlewareNotUsed()


    def __call__(self, request):
        request.current_site, request.current_shop = get_current_site_and_shop(request)
        if request.user.is_authenticated:
            log_session_info('DatabaseUserMiddleware.__call__.aboutToSetUser')
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT set_config('shop.current_user_id', %s, FALSE)",
                    [str(request.user.id)]
                )
            log_session_info('DatabaseUserMiddleware.__call__userIsSet')
        response = self.get_response(request)
        return response
    
# class ForwardedPortMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
        
#         forwarded_port = request.META.get('HTTP_X_FORWARDED_PORT')
#         domain = request.META.get('HTTP_X_FORWARDED_HOST')
#         scheme = request.META.get('HTTP_X_FORWARDED_PROTO')
#         if forwarded_port:
#             request.META['SERVER_PORT'] = forwarded_port
#         if domain:
#              request.META['SERVER_HOST'] = domain
#         if scheme:
#            request.META['SERVER_SCHEME'] = scheme
#         else:
#             request.META['SERVER_SCHEME'] = request.scheme
#         response = self.get_response(request)
#         return response
from django.urls import reverse
from django.http import HttpResponseForbidden
    
class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated or not request.user.is_superuser:
                return HttpResponseForbidden('<h1>403 Forbidden</h1><p>You do not have permission to access this page.</p>')
        
        response = self.get_response(request)
        return response

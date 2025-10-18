from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import re

class XSSProtectionMiddleware(MiddlewareMixin):
    """
    Middleware برای محافظت در برابر حملات XSS
    """
    
    def process_request(self, request):
        # بررسی پارامترهای GET و POST برای محتوای مشکوک
        suspicious_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>',
            r'<link[^>]*>',
            r'<meta[^>]*>',
            r'<style[^>]*>.*?</style>',
            r'expression\s*\(',
            r'url\s*\(',
            r'@import',
        ]
        
        # بررسی GET parameters
        for key, value in request.GET.items():
            if isinstance(value, str):
                for pattern in suspicious_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return HttpResponse('Suspicious content detected', status=400)
        
        # بررسی POST parameters
        if request.method == 'POST':
            for key, value in request.POST.items():
                if isinstance(value, str):
                    for pattern in suspicious_patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            return HttpResponse('Suspicious content detected', status=400)
        
        return None
    
    def process_response(self, request, response):
        # اضافه کردن هدرهای امنیتی
        response['X-XSS-Protection'] = '1; mode=block'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

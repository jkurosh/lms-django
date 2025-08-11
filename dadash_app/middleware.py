from django.http import HttpResponseForbidden
from django.conf import settings
import re

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # بررسی User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if self.is_suspicious_user_agent(user_agent):
            return HttpResponseForbidden('Access Denied')
            
        # بررسی IP
        client_ip = self.get_client_ip(request)
        if self.is_blocked_ip(client_ip):
            return HttpResponseForbidden('Access Denied')
            
        response = self.get_response(request)
        
        # اضافه کردن هدرهای امنیتی
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
        
    def is_suspicious_user_agent(self, user_agent):
        suspicious_patterns = [
            r'bot',
            r'crawler',
            r'spider',
            r'scanner',
            r'exploit',
            r'sqlmap',
            r'nmap'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, user_agent.lower()):
                return True
        return False
        
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
    def is_blocked_ip(self, ip):
        # لیست IP های مسدود شده
        blocked_ips = getattr(settings, 'BLOCKED_IPS', [])
        return ip in blocked_ips 
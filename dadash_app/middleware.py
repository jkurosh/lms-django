from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
import re
import json
import logging

logger = logging.getLogger(__name__)

class RequestPrivacyMiddleware:
    """Middleware برای مخفی کردن اطلاعات request"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # فقط در صورت استفاده از ابزارهای واقعاً مشکوک، User-Agent را تغییر دهید
        if request.META.get('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT'].lower()
            # فقط ابزارهای بسیار مشکوک را مسدود کنید (نه devtools عادی)
            if any(suspicious in user_agent for suspicious in ['sqlmap', 'nmap', 'burp', 'zap', 'wireshark']):
                request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # فقط extension های واقعاً مشکوک را مسدود کنید
        if request.META.get('HTTP_REFERER'):
            referer = request.META['HTTP_REFERER']
            # فقط extension های تحلیل شبکه را مسدود کنید
            if any(ext in referer for ext in ['burp-extension', 'wireshark-extension', 'proxy-extension']):
                request.META['HTTP_REFERER'] = request.META.get('HTTP_ORIGIN', '')
        
        response = self.get_response(request)
        
        # فقط هدرهای ضروری اضافه کنید
        response['Server'] = 'HeyVoonak'
        
        return response


class LightNetworkSecurityMiddleware:
    """Middleware ملایم برای محافظت از ابزارهای تحلیل شبکه"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # فقط ابزارهای بسیار مشکوک
        self.suspicious_tools = [
            'wireshark', 'tcpdump', 'fiddler', 'burp', 'charles', 'mitmproxy'
        ]
    
    def __call__(self, request):
        # فقط بررسی User-Agent برای ابزارهای بسیار مشکوک (بدون مسدودسازی)
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if any(tool in user_agent for tool in self.suspicious_tools):
            # فقط لاگ کن، هیچ کاری نکن
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Security tool detected: {user_agent} from IP: {self._get_client_ip(request)}")
        
        response = self.get_response(request)
        
        # فقط هدرهای امنیتی ملایم اضافه کن
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        
        return response
    
    def _get_client_ip(self, request):
        """دریافت IP واقعی کلاینت"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _is_proxy_request(self, request):
        """بررسی استفاده از proxy"""
        proxy_headers = [
            'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED', 'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED', 'HTTP_CLIENT_IP',
            'HTTP_VIA', 'HTTP_X_VIA', 'HTTP_PROXY_CONNECTION'
        ]
        
        return any(request.META.get(header) for header in proxy_headers)
    
    def _has_suspicious_headers(self, request):
        """بررسی هدرهای مشکوک"""
        suspicious_headers = [
            'HTTP_X_WIRESHARK', 'HTTP_X_TCPDUMP', 'HTTP_X_FIDDLER',
            'HTTP_X_BURP', 'HTTP_X_CHARLES', 'HTTP_X_MITMPROXY'
        ]
        
        return any(request.META.get(header) for header in suspicious_headers)
    
    def _has_suspicious_url(self, request):
        """بررسی URL های مشکوک"""
        path = request.path.lower()
        suspicious_paths = [
            '/wireshark', '/tcpdump', '/fiddler', '/burp', '/charles',
            '/mitmproxy', '/network', '/packet', '/sniffer', '/analyzer'
        ]
        
        return any(susp_path in path for susp_path in suspicious_paths)
    
    def _block_request(self, request, reason):
        """مسدود کردن درخواست"""
        from django.http import HttpResponseForbidden
        from django.utils import timezone
        
        # لاگ کردن تلاش مشکوک
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Blocked request: {reason} from IP: {self._get_client_ip(request)} at {timezone.now()}")
        
        # پاسخ مسدودسازی
        response = HttpResponseForbidden()
        response['Content-Type'] = 'text/html; charset=utf-8'
        response.content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="UTF-8">
            <title>دسترسی مسدود - HeyVoonak</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                    color: white;
                    font-family: 'Vazir', Arial, sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    text-align: center;
                }}
                .blocked-container {{
                    max-width: 500px;
                    padding: 2rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                .blocked-icon {{
                    font-size: 4rem;
                    margin-bottom: 1rem;
                    color: #ff4444;
                }}
                .blocked-title {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin-bottom: 1rem;
                    color: #ff4444;
                }}
                .blocked-message {{
                    font-size: 1rem;
                    line-height: 1.6;
                    margin-bottom: 1.5rem;
                    color: #cccccc;
                }}
            </style>
        </head>
        <body>
            <div class="blocked-container">
                <div class="blocked-icon">🚫</div>
                <div class="blocked-title">دسترسی مسدود شد</div>
                <div class="blocked-message">
                    استفاده از ابزارهای تحلیل شبکه مجاز نیست.<br>
                    لطفاً از مرورگر استاندارد استفاده کنید.
                </div>
            </div>
        </body>
        </html>
        """
        
        return response

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # لیست User-Agent های مشکوک - فقط scanner ها و exploit ها
        self.suspicious_user_agents = [
            r'sqlmap', r'nmap', r'nikto', r'havij',
            r'burp', r'zap', r'dirbuster', r'gobuster',
            r'wpscan', r'acunetix', r'nessus'
        ]
        
        # لیست IP های مسدود شده
        self.blocked_ips = getattr(settings, 'BLOCKED_IPS', [])
        
    def __call__(self, request):
        """Middleware call method"""
        
        # بررسی User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if self.is_suspicious_user_agent(user_agent):
            logger.warning(f"Suspicious user agent blocked: {user_agent} from IP: {self.get_client_ip(request)}")
            return self.create_security_response('Access Denied')
            
        # بررسی IP
        client_ip = self.get_client_ip(request)
        if self.is_blocked_ip(client_ip):
            logger.warning(f"Blocked IP attempted access: {client_ip}")
            return self.create_security_response('Access Denied')
            
        # بررسی درخواست‌های مشکوک
        if self.is_suspicious_request(request):
            logger.warning(f"Suspicious request blocked from IP: {client_ip}")
            return self.create_security_response('Access Denied')
            
        response = self.get_response(request)
        
        # اضافه کردن هدرهای امنیتی
        response = self.add_security_headers(response)
        
        return response
        
    def is_suspicious_user_agent(self, user_agent):
        """بررسی User-Agent مشکوک"""
        if not user_agent or user_agent.strip() == '':
            return False  # اجازه User-Agent خالی برای تست
            
        user_agent_lower = user_agent.lower()
        
        for pattern in self.suspicious_user_agents:
            if re.search(pattern, user_agent_lower):
                return True
                
        return False
        
    def get_client_ip(self, request):
        """دریافت IP واقعی کلاینت"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
    def is_blocked_ip(self, ip):
        """بررسی IP مسدود شده"""
        return ip in self.blocked_ips
        
    def is_suspicious_request(self, request):
        """بررسی درخواست مشکوک"""
        
        # بررسی URL های مشکوک
        path = request.path.lower()
        suspicious_paths = [
            'phpmyadmin', 'wp-admin', 'administrator',
            'backup', 'config', 'database', 'sql', 'test',
            'debug', 'info', 'status', 'phpinfo', 'shell',
            'cmd', 'exec', 'eval', 'system', 'passthru'
        ]
        
        for suspicious_path in suspicious_paths:
            if suspicious_path in path:
                return True
                
        # بررسی پارامترهای مشکوک
        query_params = request.GET
        suspicious_params = ['eval', 'exec', 'system', 'shell', 'cmd', 'script']
        
        for param in query_params:
            if any(susp in param.lower() for susp in suspicious_params):
                return True
                
        return False
        
    def add_security_headers(self, response):
        """اضافه کردن هدرهای امنیتی"""
        
        # هدرهای امنیتی اصلی
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['X-Permitted-Cross-Domain-Policies'] = 'none'
        response['Cross-Origin-Embedder-Policy'] = 'require-corp'
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Resource-Policy'] = 'same-origin'
        
        # مخفی کردن اطلاعات سرور
        response['Server'] = 'HeyVoonak'
        if 'X-Powered-By' in response:
            del response['X-Powered-By']
            
        # اضافه کردن CSP header
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response['Content-Security-Policy'] = csp_policy
        
        return response
        
    def create_security_response(self, message):
        """ایجاد پاسخ امنیتی"""
        response = HttpResponse(
            f'<html><body><h1>{message}</h1></body></html>',
            status=403,
            content_type='text/html'
        )
        
        # اضافه کردن هدرهای امنیتی
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
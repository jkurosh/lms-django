"""
Rate Limiting Middleware برای محافظت در برابر حملات DDoS
"""

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import time
from datetime import datetime, timedelta

class RateLimitMiddleware:
    """
    Middleware برای محدود کردن تعداد درخواست‌ها
    
    تنظیمات در settings.py:
    - RATE_LIMIT_ENABLED: فعال/غیرفعال کردن
    - RATE_LIMIT_MAX_REQUESTS: حداکثر تعداد درخواست
    - RATE_LIMIT_WINDOW_SECONDS: بازه زمانی (ثانیه)
    - RATE_LIMIT_BLOCK_DURATION: مدت زمان مسدود کردن (ثانیه)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # تنظیمات پیش‌فرض
        self.enabled = getattr(settings, 'RATE_LIMIT_ENABLED', True)
        self.max_requests = getattr(settings, 'RATE_LIMIT_MAX_REQUESTS', 100)
        self.window_seconds = getattr(settings, 'RATE_LIMIT_WINDOW_SECONDS', 60)
        self.block_duration = getattr(settings, 'RATE_LIMIT_BLOCK_DURATION', 300)  # 5 دقیقه
        
        # Endpoint های حساس (محدودیت بیشتر)
        self.sensitive_endpoints = {
            '/login/': {'max_requests': 30, 'window': 60},
            '/register/': {'max_requests': 20, 'window': 60},
            '/api/': {'max_requests': 200, 'window': 60},
        }
    
    def __call__(self, request):
        # اگر غیرفعال است، ادامه بده
        if not self.enabled:
            return self.get_response(request)
        
        # مسیرهایی که نیاز به Rate Limit ندارند
        exempt_paths = [
            '/static/',
            '/media/',
            '/admin/',  # برای ادمین‌ها
        ]
        
        # بررسی اینکه آیا مسیر از Rate Limit معاف است
        for exempt_path in exempt_paths:
            if request.path.startswith(exempt_path):
                return self.get_response(request)
        
        # اگر کاربر ادمین است، معاف است
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)
        
        # دریافت IP کاربر
        ip_address = self.get_client_ip(request)
        
        # بررسی اینکه آیا IP مسدود شده است
        if self.is_blocked(ip_address):
            return self.blocked_response(request, ip_address)
        
        # بررسی Rate Limit
        if not self.check_rate_limit(request, ip_address):
            # مسدود کردن IP برای مدتی
            self.block_ip(ip_address)
            return self.rate_limit_exceeded_response(request, ip_address)
        
        response = self.get_response(request)
        
        # اضافه کردن header های Rate Limit
        remaining = self.get_remaining_requests(request, ip_address)
        response['X-RateLimit-Limit'] = str(self.get_max_requests(request.path))
        response['X-RateLimit-Remaining'] = str(max(0, remaining))
        response['X-RateLimit-Reset'] = str(int(time.time()) + self.get_window_seconds(request.path))
        
        return response
    
    def get_client_ip(self, request):
        """دریافت IP واقعی کاربر"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_max_requests(self, path):
        """دریافت حداکثر تعداد درخواست برای مسیر"""
        for endpoint, limits in self.sensitive_endpoints.items():
            if path.startswith(endpoint):
                return limits['max_requests']
        return self.max_requests
    
    def get_window_seconds(self, path):
        """دریافت بازه زمانی برای مسیر"""
        for endpoint, limits in self.sensitive_endpoints.items():
            if path.startswith(endpoint):
                return limits['window']
        return self.window_seconds
    
    def check_rate_limit(self, request, ip_address):
        """بررسی اینکه آیا کاربر از محدودیت تجاوز کرده"""
        path = request.path
        max_requests = self.get_max_requests(path)
        window = self.get_window_seconds(path)
        
        # کلید برای cache
        cache_key = self.get_rate_limit_key(ip_address, path)
        
        try:
            # دریافت تعداد درخواست‌های فعلی
            request_count = cache.get(cache_key, 0)
            
            if request_count >= max_requests:
                self.log_rate_limit_event(ip_address, path, 'exceeded')
                return False
            
            # افزایش شمارنده
            cache.set(cache_key, request_count + 1, window)
            
            return True
        
        except Exception as e:
            # اگر مشکلی در cache بود، اجازه دسترسی بده
            print(f"[Rate Limit Error] {str(e)}")
            return True
    
    def get_remaining_requests(self, request, ip_address):
        """دریافت تعداد درخواست‌های باقی‌مانده"""
        path = request.path
        max_requests = self.get_max_requests(path)
        cache_key = self.get_rate_limit_key(ip_address, path)
        
        try:
            request_count = cache.get(cache_key, 0)
            return max_requests - request_count
        except:
            return max_requests
    
    def is_blocked(self, ip_address):
        """بررسی اینکه آیا IP مسدود شده"""
        cache_key = f'blocked_ip:{ip_address}'
        try:
            return cache.get(cache_key, False)
        except:
            return False
    
    def block_ip(self, ip_address):
        """مسدود کردن IP برای مدتی"""
        cache_key = f'blocked_ip:{ip_address}'
        try:
            cache.set(cache_key, True, self.block_duration)
            # ثبت لاگ
            self.log_rate_limit_event(ip_address, '', 'blocked')
        except Exception as e:
            print(f"[Rate Limit Error] Could not block IP: {str(e)}")
    
    def rate_limit_exceeded_response(self, request, ip_address):
        """پاسخ برای زمانی که از محدودیت تجاوز شده"""
        retry_after = self.get_window_seconds(request.path)
        
        # ثبت لاگ
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ Rate Limit تجاوز شد: {ip_address} - {request.path}")
        
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است',
                'message': f'لطفاً {retry_after} ثانیه صبر کنید',
                'retry_after': retry_after,
                'blocked_until': datetime.now() + timedelta(seconds=self.block_duration)
            }, status=429)
        
        html_response = f"""
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>محدودیت درخواست</title>
            <style>
                body {{
                    font-family: 'Tahoma', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    padding: 3rem;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                    max-width: 500px;
                }}
                .icon {{
                    font-size: 4rem;
                    margin-bottom: 1rem;
                }}
                h1 {{
                    color: #ef4444;
                    margin-bottom: 1rem;
                }}
                p {{
                    color: #64748b;
                    line-height: 1.8;
                    margin-bottom: 1.5rem;
                }}
                .timer {{
                    background: #fef2f2;
                    color: #ef4444;
                    padding: 1rem;
                    border-radius: 10px;
                    font-size: 1.2rem;
                    font-weight: bold;
                    margin: 1rem 0;
                }}
                .btn {{
                    background: linear-gradient(135deg, #3EA66B 0%, #2d8a54 100%);
                    color: white;
                    padding: 0.75rem 2rem;
                    border: none;
                    border-radius: 10px;
                    font-size: 1rem;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 1rem;
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(62, 166, 107, 0.3);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🚫</div>
                <h1>تعداد درخواست‌های شما بیش از حد مجاز است!</h1>
                <p>
                    شما از محدودیت تعداد درخواست‌ها تجاوز کرده‌اید.
                    <br>
                    لطفاً کمی صبر کنید و سپس دوباره تلاش کنید.
                </p>
                <div class="timer" id="timer">
                    لطفاً {self.block_duration // 60} دقیقه صبر کنید
                </div>
                <p style="font-size: 0.9rem; color: #94a3b8;">
                    IP شما: {ip_address}
                    <br>
                    زمان باز شدن: {(datetime.now() + timedelta(seconds=self.block_duration)).strftime('%H:%M:%S')}
                </p>
                <a href="/" class="btn">بازگشت به صفحه اصلی</a>
            </div>
            <script>
                // Countdown timer
                let seconds = {self.block_duration};
                const timerEl = document.getElementById('timer');
                
                setInterval(() => {{
                    if (seconds > 0) {{
                        const minutes = Math.floor(seconds / 60);
                        const secs = seconds % 60;
                        timerEl.textContent = `${{minutes}}:${{secs.toString().padStart(2, '0')}} باقی‌مانده`;
                        seconds--;
                    }} else {{
                        timerEl.textContent = 'می‌توانید دوباره تلاش کنید!';
                        timerEl.style.background = '#dcfce7';
                        timerEl.style.color = '#22c55e';
                    }}
                }}, 1000);
            </script>
        </body>
        </html>
        """
        
        response = HttpResponse(html_response, status=429)
        response['Retry-After'] = str(retry_after)
        return response
    
    def blocked_response(self, request, ip_address):
        """پاسخ برای IP های مسدود شده"""
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'IP شما به دلیل تجاوز از محدودیت‌ها مسدود شده است',
                'message': f'لطفاً {self.block_duration // 60} دقیقه صبر کنید',
                'blocked': True
            }, status=403)
        
        html_response = f"""
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>دسترسی مسدود شده</title>
            <style>
                body {{
                    font-family: 'Tahoma', sans-serif;
                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    padding: 3rem;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
                    text-align: center;
                    max-width: 500px;
                }}
                .icon {{
                    font-size: 5rem;
                    margin-bottom: 1rem;
                }}
                h1 {{
                    color: #dc2626;
                    margin-bottom: 1rem;
                    font-size: 1.8rem;
                }}
                p {{
                    color: #64748b;
                    line-height: 1.8;
                    margin-bottom: 1.5rem;
                }}
                .warning-box {{
                    background: #fef2f2;
                    border: 2px solid #fecaca;
                    color: #991b1b;
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin: 1.5rem 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🔒</div>
                <h1>دسترسی شما مسدود شده است!</h1>
                <p>
                    به دلیل تعداد بالای درخواست‌های مشکوک،
                    <br>
                    دسترسی شما برای مدتی محدود شده است.
                </p>
                <div class="warning-box">
                    <strong>⚠️ توجه:</strong>
                    <br>
                    اگر فکر می‌کنید این یک اشتباه است، لطفاً با پشتیبانی تماس بگیرید.
                </div>
                <p style="font-size: 0.85rem; color: #94a3b8;">
                    IP: {ip_address}
                    <br>
                    زمان رفع مسدودیت: {(datetime.now() + timedelta(seconds=self.block_duration)).strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_response, status=403)
    
    def get_rate_limit_key(self, ip_address, path):
        """ساخت کلید برای cache"""
        # برای endpoint های حساس، کلید جداگانه
        for endpoint in self.sensitive_endpoints.keys():
            if path.startswith(endpoint):
                return f'rate_limit:{ip_address}:{endpoint}'
        
        # برای بقیه endpoint ها
        return f'rate_limit:{ip_address}:general'
    
    def log_rate_limit_event(self, ip_address, path, event_type='warning'):
        """ثبت لاگ رویدادهای Rate Limit"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if event_type == 'blocked':
            print(f"[{timestamp}] 🚫 BLOCKED: IP {ip_address} مسدود شد - {path}")
        elif event_type == 'exceeded':
            print(f"[{timestamp}] ⚠️  RATE LIMIT: IP {ip_address} از محدودیت تجاوز کرد - {path}")
        elif event_type == 'suspicious':
            print(f"[{timestamp}] 👁️  SUSPICIOUS: فعالیت مشکوک از IP {ip_address} - {path}")


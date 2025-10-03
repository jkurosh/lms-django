from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
import time

def require_authentication(view_func):
    """Decorator برای احراز هویت اجباری"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Authentication required'}, status=401)
            messages.error(request, 'لطفاً ابتدا وارد شوید.')
            return redirect('heyvoonak:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def require_staff(view_func):
    """Decorator برای دسترسی staff اجباری"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Authentication required'}, status=401)
            messages.error(request, 'لطفاً ابتدا وارد شوید.')
            return redirect('heyvoonak:login')
        
        if not request.user.is_staff:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Staff access required'}, status=403)
            messages.error(request, 'شما دسترسی به این صفحه را ندارید.')
            return redirect('heyvoonak:landing_page')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def rate_limit(max_requests=10, window_seconds=60):
    """Decorator برای محدود کردن درخواست‌ها"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # شناسایی کاربر
            if request.user.is_authenticated:
                identifier = f"user_{request.user.id}"
            else:
                identifier = f"ip_{request.META.get('REMOTE_ADDR', 'unknown')}"
            
            # بررسی cache
            cache_key = f"rate_limit_{identifier}"
            requests = cache.get(cache_key, [])
            
            # حذف درخواست‌های قدیمی
            current_time = time.time()
            requests = [req_time for req_time in requests if current_time - req_time < window_seconds]
            
            # بررسی محدودیت
            if len(requests) >= max_requests:
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
                messages.error(request, 'تعداد درخواست‌ها بیش از حد مجاز است. لطفاً کمی صبر کنید.')
                return redirect('heyvoonak:landing_page')
            
            # اضافه کردن درخواست فعلی
            requests.append(current_time)
            cache.set(cache_key, requests, window_seconds)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def secure_headers(view_func):
    """Decorator برای اضافه کردن هدرهای امنیتی"""
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        # اضافه کردن هدرهای امنیتی
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; img-src 'self' data:; font-src 'self' cdnjs.cloudflare.com;"
        
        return response
    return wrapper

# Decorators for subscription system
def subscription_required_or_admin(view_func):
    """Decorator برای بررسی اشتراک یا دسترسی admin"""
    def wrapper(request, *args, **kwargs):
        # اگر کاربر admin است، اجازه دسترسی
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        
        # اگر کاربر لاگین نکرده، به صفحه ورود هدایت شود
        if not request.user.is_authenticated:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Authentication required'}, status=401)
            from django.shortcuts import redirect
            return redirect('heyvoonak:login')
        
        # بررسی اشتراک فعال
        from .models import Subscription
        try:
            subscription = Subscription.objects.filter(
                user=request.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()
            
            if not subscription:
                # کاربر اشتراک فعال ندارد
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'error': 'Active subscription required'}, status=403)
                from django.shortcuts import render
                return render(request, 'dadash/no_subscription.html')
                
        except Exception as e:
            # در صورت خطا، اجازه دسترسی نده
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Subscription check failed'}, status=500)
            from django.shortcuts import render
            return render(request, 'dadash/no_subscription.html')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def subscription_required(view_func):
    """Decorator برای بررسی اشتراک (بدون دسترسی admin)"""
    def wrapper(request, *args, **kwargs):
        # اگر کاربر لاگین نکرده، به صفحه ورود هدایت شود
        if not request.user.is_authenticated:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Authentication required'}, status=401)
            from django.shortcuts import redirect
            return redirect('heyvoonak:login')
        
        # بررسی اشتراک فعال
        from .models import Subscription
        try:
            subscription = Subscription.objects.filter(
                user=request.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()
            
            if not subscription:
                # کاربر اشتراک فعال ندارد
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'error': 'Active subscription required'}, status=403)
                from django.shortcuts import render
                return render(request, 'dadash/no_subscription.html')
                
        except Exception as e:
            # در صورت خطا، اجازه دسترسی نده
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Subscription check failed'}, status=500)
            from django.shortcuts import render
            return render(request, 'dadash/no_subscription.html')
        
        return view_func(request, *args, **kwargs)
    return wrapper
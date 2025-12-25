"""
Context processors برای دسترسی به داده‌ها در همه template ها
"""
from django.db import OperationalError, DatabaseError
from .models import Cart


def cart_context(request):
    """اضافه کردن اطلاعات سبد خرید به context"""
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.items_count
        except Cart.DoesNotExist:
            cart_count = 0
        except (OperationalError, DatabaseError):
            # در صورت قطع اتصال دیتابیس، مقدار پیش‌فرض را برمی‌گردانیم
            cart_count = 0
    
    return {
        'cart_count': cart_count
    }


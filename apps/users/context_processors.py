"""
Context processors برای دسترسی به داده‌ها در همه template ها
"""
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
    
    return {
        'cart_count': cart_count
    }


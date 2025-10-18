"""
View های مربوط به سبد خرید
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem, SubscriptionPlan


@login_required
def view_cart(request):
    """نمایش سبد خرید"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('plan').all(),
        'total_price': cart.total_price,
    }
    
    return render(request, 'users/cart.html', context)


@login_required
def add_to_cart(request, plan_id):
    """افزودن به سبد خرید"""
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # بررسی اینکه آیا این پلن قبلاً در سبد هست
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        plan=plan,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        # اگر قبلاً در سبد بود، تعداد را افزایش نمی‌دهیم
        # چون اشتراک معمولاً یکبار خریداری می‌شود
        messages.info(request, 'این پلن قبلاً به سبد خرید اضافه شده است.')
    else:
        messages.success(request, f'{plan.name} به سبد خرید اضافه شد.')
    
    # اگر درخواست AJAX است
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.items_count,
            'message': 'به سبد خرید اضافه شد'
        })
    
    return redirect('users:view_cart')


@login_required
def remove_from_cart(request, item_id):
    """حذف از سبد خرید"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    plan_name = cart_item.plan.name
    cart_item.delete()
    
    messages.success(request, f'{plan_name} از سبد خرید حذف شد.')
    
    # اگر درخواست AJAX است
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.items_count,
            'message': 'از سبد خرید حذف شد'
        })
    
    return redirect('users:view_cart')


@login_required
def update_cart_item(request, item_id):
    """به‌روزرسانی تعداد آیتم سبد"""
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'تعداد به‌روزرسانی شد.')
        else:
            cart_item.delete()
            messages.success(request, 'آیتم از سبد حذف شد.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.items_count,
                'total_price': float(cart.total_price),
            })
    
    return redirect('users:view_cart')


@login_required
def clear_cart(request):
    """خالی کردن سبد خرید"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.clear()
    
    messages.success(request, 'سبد خرید خالی شد.')
    return redirect('users:view_cart')


def get_cart_count(request):
    """دریافت تعداد آیتم‌های سبد (برای AJAX)"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.items_count
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0
    
    return JsonResponse({'count': count})


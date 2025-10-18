"""
ویوهای پرداخت با زرین‌پال
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from zarinpal import ZarinPal
from .zarinpal_config import ZarinpalConfig
from .models import Payment, SubscriptionPlan, Subscription, Cart
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """دریافت IP کاربر"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def initiate_payment(request, plan_id):
    """
    ایجاد درخواست پرداخت
    """
    try:
        # دریافت پلن
        plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
        
        # محاسبه مبلغ نهایی (به ریال)
        amount_tomans = int(plan.final_price)
        amount_rials = amount_tomans * 10  # تبدیل تومان به ریال
        
        # ایجاد رکورد پرداخت
        payment = Payment.objects.create(
            user=request.user,
            amount=amount_tomans,
            gateway='zarinpal',
            status='pending',
            description=f'خرید اشتراک {plan.name}',
            ip_address=get_client_ip(request)
        )
        
        # پیکربندی زرین‌پال
        config_dict = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'sandbox': settings.ZARINPAL_SANDBOX,
        }
        
        zarinpal = ZarinPal(config_dict)
        
        # URL بازگشت
        callback_url = request.build_absolute_uri(
            reverse('users:payment_callback')
        )
        
        # ارسال درخواست به زرین‌پال
        response = zarinpal.payments.create({
            "amount": amount_rials,
            "callback_url": callback_url,
            "description": payment.description,
            "mobile": request.user.phone_number if hasattr(request.user, 'phone_number') else None,
            "email": request.user.email if request.user.email else None,
        })
        
        logger.info(f"Zarinpal response: {response}")
        
        # بررسی پاسخ
        if "data" in response and "authority" in response["data"]:
            authority = response["data"]["authority"]
            
            # ذخیره Authority در دیتابیس
            payment.authority = authority
            payment.save()
            
            # ایجاد URL پرداخت
            payment_url = zarinpal.payments.generate_payment_url(authority)
            
            logger.info(f"Payment URL generated: {payment_url}")
            
            # هدایت به درگاه پرداخت
            return redirect(payment_url)
        else:
            logger.error(f"Zarinpal error: {response}")
            payment.mark_as_failed()
            messages.error(request, 'خطا در ایجاد درخواست پرداخت. لطفاً دوباره تلاش کنید.')
            return redirect('users:subscription_plans')
            
    except Exception as e:
        logger.error(f"Payment initiation error: {e}")
        messages.error(request, f'خطا در فرآیند پرداخت: {str(e)}')
        return redirect('users:subscription_plans')


@csrf_exempt
def payment_callback(request):
    """
    Callback پس از پرداخت (تأیید پرداخت)
    """
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    
    logger.info(f"Payment callback - Authority: {authority}, Status: {status}")
    
    if not authority:
        messages.error(request, 'اطلاعات پرداخت نامعتبر است.')
        return redirect('users:subscription_plans')
    
    try:
        # پیدا کردن پرداخت
        payment = get_object_or_404(Payment, authority=authority)
        
        if status == 'OK':
            # پیکربندی زرین‌پال
            config_dict = {
                'merchant_id': settings.ZARINPAL_MERCHANT_ID,
                'sandbox': settings.ZARINPAL_SANDBOX,
            }
            
            zarinpal = ZarinPal(config_dict)
            
            # تبدیل تومان به ریال
            amount_rials = int(payment.amount) * 10
            
            # تأیید پرداخت
            response = zarinpal.verifications.verify({
                "amount": amount_rials,
                "authority": authority,
            })
            
            logger.info(f"Verification response: {response}")
            
            # بررسی نتیجه تأیید
            if response.get("data", {}).get("code") in [100, 101]:
                # کد 100: پرداخت موفق
                # کد 101: پرداخت قبلاً تأیید شده
                
                ref_id = response["data"].get("ref_id")
                card_pan = response["data"].get("card_pan")
                fee = response["data"].get("fee")
                
                # به‌روزرسانی پرداخت
                payment.mark_as_paid(ref_id=ref_id, card_number=card_pan)
                
                # ایجاد یا به‌روزرسانی اشتراک
                subscription, created = Subscription.objects.get_or_create(
                    user=payment.user,
                    defaults={
                        'subscription_type': 'premium',
                        'status': 'active',
                        'price': payment.amount,
                        'payment_method': 'online',
                        'transaction_id': ref_id,
                        'auto_renew': False,
                    }
                )
                
                if not created:
                    subscription.status = 'active'
                    subscription.transaction_id = ref_id
                    subscription.save()
                
                # ارتباط پرداخت با اشتراک
                payment.subscription = subscription
                payment.save()
                
                logger.info(f"Payment successful - Ref ID: {ref_id}")
                
                # خالی کردن سبد خرید (اگر از سبد خرید بود)
                if 'cart_payment_id' in request.session:
                    try:
                        cart = Cart.objects.get(user=payment.user)
                        cart.items.all().delete()  # حذف تمام آیتم‌ها
                        del request.session['cart_payment_id']
                        logger.info(f"Cart cleared after successful payment")
                    except Cart.DoesNotExist:
                        pass
                
                # پیام موفقیت
                messages.success(
                    request,
                    f'پرداخت با موفقیت انجام شد! شماره پیگیری: {ref_id}'
                )
                return redirect('users:payment_success', payment_id=payment.id)
            else:
                # پرداخت ناموفق
                payment.mark_as_failed()
                code = response.get("data", {}).get("code")
                logger.error(f"Payment verification failed - Code: {code}")
                messages.error(request, f'پرداخت ناموفق بود. کد خطا: {code}')
                return redirect('users:payment_failed', payment_id=payment.id)
        else:
            # کاربر پرداخت را لغو کرده
            payment.status = 'cancelled'
            payment.save()
            logger.info(f"Payment cancelled by user - Authority: {authority}")
            messages.warning(request, 'پرداخت توسط شما لغو شد.')
            return redirect('users:subscription_plans')
            
    except Payment.DoesNotExist:
        logger.error(f"Payment not found - Authority: {authority}")
        messages.error(request, 'پرداخت مورد نظر یافت نشد.')
        return redirect('users:subscription_plans')
    except Exception as e:
        logger.error(f"Payment callback error: {e}")
        messages.error(request, f'خطا در تأیید پرداخت: {str(e)}')
        return redirect('users:subscription_plans')


@login_required
def payment_success(request, payment_id):
    """صفحه موفقیت پرداخت"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'users/payment_success.html', context)


@login_required
def payment_failed(request, payment_id):
    """صفحه شکست پرداخت"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'users/payment_failed.html', context)


@login_required
def checkout_from_cart(request):
    """
    پرداخت از سبد خرید
    """
    try:
        # دریافت سبد خرید کاربر
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.warning(request, 'سبد خرید شما خالی است.')
            return redirect('users:view_cart')
        
        # محاسبه مبلغ کل (به تومان)
        total_amount = int(cart.total_price)
        amount_rials = total_amount * 10  # تبدیل تومان به ریال
        
        # ایجاد رکورد پرداخت
        payment = Payment.objects.create(
            user=request.user,
            amount=total_amount,
            gateway='zarinpal',
            status='pending',
            description=f'خرید {cart.items_count} پلن اشتراک',
            ip_address=get_client_ip(request)
        )
        
        # پیکربندی زرین‌پال
        config_dict = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'sandbox': settings.ZARINPAL_SANDBOX,
        }
        
        zarinpal = ZarinPal(config_dict)
        
        # URL بازگشت
        callback_url = request.build_absolute_uri(
            reverse('users:payment_callback')
        )
        
        # ارسال درخواست به زرین‌پال
        response = zarinpal.payments.create({
            "amount": amount_rials,
            "callback_url": callback_url,
            "description": payment.description,
            "mobile": request.user.phone_number if hasattr(request.user, 'phone_number') else None,
            "email": request.user.email if request.user.email else None,
        })
        
        logger.info(f"Zarinpal cart checkout response: {response}")
        
        # بررسی پاسخ
        if "data" in response and "authority" in response["data"]:
            authority = response["data"]["authority"]
            
            # ذخیره Authority در دیتابیس
            payment.authority = authority
            payment.save()
            
            # ذخیره شناسه payment در session برای بعد از پرداخت
            request.session['cart_payment_id'] = payment.id
            
            # ایجاد URL پرداخت
            payment_url = zarinpal.payments.generate_payment_url(authority)
            
            logger.info(f"Cart payment URL generated: {payment_url}")
            
            # هدایت به درگاه پرداخت
            return redirect(payment_url)
        else:
            logger.error(f"Zarinpal error: {response}")
            payment.mark_as_failed()
            messages.error(request, 'خطا در ایجاد درخواست پرداخت. لطفاً دوباره تلاش کنید.')
            return redirect('users:view_cart')
            
    except Exception as e:
        logger.error(f"Cart checkout error: {e}")
        messages.error(request, f'خطا در فرآیند پرداخت: {str(e)}')
        return redirect('users:view_cart')


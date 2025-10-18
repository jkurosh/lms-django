"""
API Views برای پرداخت با زرین‌پال SDK
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .services.zarinpal_sdk import zarinpal_service
from .models import Payment
from .services.sms_service import sms_service


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    """
    ایجاد درخواست پرداخت
    
    Body:
    {
        "amount": 100000,  // مبلغ به ریال
        "description": "خرید دوره آموزشی",
        "mobile": "09123456789"  // اختیاری
    }
    """
    user = request.user
    amount = request.data.get('amount')
    description = request.data.get('description', 'پرداخت')
    mobile = request.data.get('mobile')
    
    # اعتبارسنجی
    if not amount:
        return Response({
            'success': False,
            'error': 'مبلغ الزامی است'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        amount = int(amount)
        if amount < 1000:
            return Response({
                'success': False,
                'error': 'حداقل مبلغ 1000 ریال است'
            }, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({
            'success': False,
            'error': 'مبلغ نامعتبر است'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # ساخت URL بازگشت
    callback_url = request.build_absolute_uri('/api/v1/payment/verify/')
    
    # ایجاد درخواست پرداخت
    result = zarinpal_service.create_payment(
        amount=amount,
        callback_url=callback_url,
        description=description,
        mobile=mobile or getattr(user.profile, 'phone_number', None)
    )
    
    if result['success']:
        # ذخیره در دیتابیس
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            authority=result['authority'],
            description=description,
            status='pending'
        )
        
        return Response({
            'success': True,
            'payment_id': payment.id,
            'authority': result['authority'],
            'payment_url': result['payment_url'],
            'message': 'درخواست پرداخت ایجاد شد'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'error': result.get('error', 'خطا در ایجاد درخواست پرداخت')
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    """
    تایید پرداخت (callback از زرین‌پال)
    
    Query Parameters:
    - Authority: کد authority
    - Status: وضعیت (OK یا NOK)
    """
    authority = request.GET.get('Authority') or request.data.get('authority')
    payment_status = request.GET.get('Status') or request.data.get('status')
    
    if not authority:
        return Response({
            'success': False,
            'error': 'کد Authority یافت نشد'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # پیدا کردن پرداخت
    try:
        payment = Payment.objects.get(authority=authority)
    except Payment.DoesNotExist:
        return Response({
            'success': False,
            'error': 'پرداخت یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # بررسی وضعیت
    if payment_status != 'OK':
        payment.status = 'failed'
        payment.save()
        
        return Response({
            'success': False,
            'error': 'پرداخت توسط کاربر لغو شد',
            'payment_id': payment.id
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # تایید پرداخت
    result = zarinpal_service.verify_payment(authority, payment.amount)
    
    if result['success'] and result['verified']:
        # به‌روزرسانی پرداخت
        payment.status = 'verified'
        payment.ref_id = result.get('ref_id')
        payment.card_pan = result.get('card_pan')
        payment.fee = result.get('fee')
        payment.verified_at = timezone.now()
        payment.save()
        
        # ارسال پیامک خرید موفق
        try:
            if hasattr(payment.user, 'profile') and payment.user.profile.phone_number:
                sms_result = sms_service.send_purchase_success(
                    phone_number=payment.user.profile.phone_number,
                    order_id=f"PAY-{payment.id}",
                    amount=int(payment.amount)
                )
                print(f"SMS sent: {sms_result}")
        except Exception as e:
            print(f"Error sending SMS: {e}")
        
        return Response({
            'success': True,
            'verified': True,
            'payment_id': payment.id,
            'ref_id': result.get('ref_id'),
            'card_pan': result.get('card_pan'),
            'fee': result.get('fee'),
            'message': result.get('message', 'پرداخت با موفقیت تایید شد')
        }, status=status.HTTP_200_OK)
    else:
        payment.status = 'failed'
        payment.save()
        
        return Response({
            'success': False,
            'verified': False,
            'error': result.get('error', 'تایید پرداخت ناموفق بود'),
            'payment_id': payment.id
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_fee(request):
    """
    محاسبه کارمزد تراکنش
    
    Body:
    {
        "amount": 100000
    }
    """
    amount = request.data.get('amount')
    
    if not amount:
        return Response({
            'success': False,
            'error': 'مبلغ الزامی است'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # محاسبه کارمزد زرین‌پال (حدود 1%)
    try:
        amount_int = int(amount)
        fee = int(amount_int * 0.01)  # 1% کارمزد
        total = amount_int + fee
        
        return Response({
            'success': True,
            'amount': amount_int,
            'fee': fee,
            'total': total
        }, status=status.HTTP_200_OK)
    except ValueError:
        return Response({
            'success': False,
            'error': 'مبلغ نامعتبر است'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_list(request):
    """
    لیست پرداخت‌های کاربر
    """
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    payment_data = []
    for payment in payments:
        payment_data.append({
            'id': payment.id,
            'amount': payment.amount,
            'authority': payment.authority,
            'ref_id': payment.ref_id,
            'status': payment.status,
            'description': payment.description,
            'created_at': payment.created_at,
            'verified_at': payment.verified_at
        })
    
    return Response({
        'success': True,
        'payments': payment_data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_detail(request, payment_id):
    """
    جزئیات یک پرداخت
    """
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    return Response({
        'success': True,
        'payment': {
            'id': payment.id,
            'amount': payment.amount,
            'authority': payment.authority,
            'ref_id': payment.ref_id,
            'card_pan': payment.card_pan,
            'fee': payment.fee,
            'status': payment.status,
            'description': payment.description,
            'created_at': payment.created_at,
            'verified_at': payment.verified_at
        }
    }, status=status.HTTP_200_OK)

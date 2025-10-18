from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone

from .auth_serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PurchaseNotificationSerializer
)
from .auth_models import PurchaseNotification
from .services.sms_service import sms_service


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    """
    ارسال کد OTP
    
    Body:
    {
        "phone_number": "09123456789",
        "purpose": "register" | "login" | "password_reset"
    }
    """
    serializer = SendOTPSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'کد تایید با موفقیت ارسال شد'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    تایید کد OTP
    
    Body:
    {
        "phone_number": "09123456789",
        "otp_code": "123456",
        "purpose": "register" | "login" | "password_reset"
    }
    """
    serializer = VerifyOTPSerializer(data=request.data)
    
    if serializer.is_valid():
        return Response({
            'success': True,
            'message': 'کد تایید صحیح است'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    ثبت‌نام با شماره موبایل و OTP
    
    Body:
    {
        "phone_number": "09123456789",
        "otp_code": "123456",
        "username": "user123",
        "password": "password123",
        "first_name": "نام",
        "last_name": "نام خانوادگی"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # ایجاد توکن JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'ثبت‌نام با موفقیت انجام شد',
            'user': {
                'id': user.id,
                'username': user.username,
                'phone_number': user.auth_profile.phone_number if hasattr(user, 'auth_profile') else '',
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_otp(request):
    """
    ورود با شماره موبایل و OTP
    
    Body:
    {
        "phone_number": "09123456789",
        "otp_code": "123456"
    }
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # ایجاد توکن JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'ورود با موفقیت انجام شد',
            'user': {
                'id': user.id,
                'username': user.username,
                'phone_number': user.auth_profile.phone_number if hasattr(user, 'auth_profile') else '',
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """
    بازیابی رمز عبور
    
    Body:
    {
        "phone_number": "09123456789",
        "otp_code": "123456",
        "new_password": "newpassword123"
    }
    """
    serializer = PasswordResetSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        return Response({
            'success': True,
            'message': 'رمز عبور با موفقیت تغییر یافت'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_purchase_notification(request):
    """
    ارسال اعلان خرید موفق
    
    Body:
    {
        "order_id": "ORD123456",
        "amount": 150000
    }
    """
    user = request.user
    order_id = request.data.get('order_id')
    amount = request.data.get('amount')
    
    if not order_id or not amount:
        return Response({
            'success': False,
            'error': 'شماره سفارش و مبلغ الزامی است'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # دریافت شماره موبایل از پروفایل
        phone_number = user.profile.phone_number
        
        # ارسال پیامک
        result = sms_service.send_purchase_success(phone_number, order_id, int(amount))
        
        # ذخیره اعلان
        notification = PurchaseNotification.objects.create(
            user=user,
            phone_number=phone_number,
            order_id=order_id,
            amount=amount,
            is_sent=result['success'],
            sent_at=timezone.now() if result['success'] else None
        )
        
        if result['success']:
            return Response({
                'success': True,
                'message': 'اعلان خرید با موفقیت ارسال شد',
                'notification_id': notification.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'خطا در ارسال پیامک')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchase_notifications(request):
    """
    دریافت لیست اعلان‌های خرید کاربر
    """
    notifications = PurchaseNotification.objects.filter(user=request.user)
    serializer = PurchaseNotificationSerializer(notifications, many=True)
    
    return Response({
        'success': True,
        'notifications': serializer.data
    }, status=status.HTTP_200_OK)

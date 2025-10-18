from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .auth_models import OTPVerification, UserProfile, PurchaseNotification
from .services.sms_service import sms_service

class SendOTPSerializer(serializers.Serializer):
    """
    سریالایزر ارسال کد OTP
    """
    phone_number = serializers.CharField(max_length=11, required=True)
    purpose = serializers.ChoiceField(
        choices=['register', 'login', 'password_reset'],
        required=True
    )
    
    def validate_phone_number(self, value):
        """
        اعتبارسنجی شماره موبایل
        """
        if not value.isdigit() or len(value) != 11 or not value.startswith('09'):
            raise serializers.ValidationError('شماره موبایل نامعتبر است')
        return value
    
    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        purpose = validated_data['purpose']
        
        # بررسی محدودیت ارسال (حداکثر 3 بار در ساعت)
        recent_otps = OTPVerification.objects.filter(
            phone_number=phone_number,
            purpose=purpose,
            created_at__gte=timezone.now() - timedelta(hours=1)
        ).count()
        
        if recent_otps >= 3:
            raise serializers.ValidationError('محدودیت ارسال کد. لطفاً بعداً تلاش کنید.')
        
        # ارسال کد OTP
        result = sms_service.send_otp_and_cache(phone_number, purpose)
        
        if not result['success']:
            raise serializers.ValidationError(result.get('error', 'خطا در ارسال پیامک'))
        
        return validated_data


class VerifyOTPSerializer(serializers.Serializer):
    """
    سریالایزر تایید کد OTP
    """
    phone_number = serializers.CharField(max_length=11, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    purpose = serializers.ChoiceField(
        choices=['register', 'login', 'password_reset'],
        required=True
    )
    
    def validate(self, attrs):
        phone_number = attrs['phone_number']
        otp_code = attrs['otp_code']
        purpose = attrs['purpose']
        
        # تایید کد OTP
        result = sms_service.verify_otp(phone_number, otp_code, purpose)
        
        if not result['success']:
            raise serializers.ValidationError(result.get('error', 'کد تایید نادرست است'))
        
        return attrs


class RegisterSerializer(serializers.Serializer):
    """
    سریالایزر ثبت‌نام با شماره موبایل
    """
    phone_number = serializers.CharField(max_length=11, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    
    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 11 or not value.startswith('09'):
            raise serializers.ValidationError('شماره موبایل نامعتبر است')
        
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('این شماره موبایل قبلاً ثبت شده است')
        
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('این نام کاربری قبلاً ثبت شده است')
        return value
    
    def validate(self, attrs):
        # تایید کد OTP
        result = sms_service.verify_otp(
            attrs['phone_number'],
            attrs['otp_code'],
            'register'
        )
        
        if not result['success']:
            raise serializers.ValidationError({'otp_code': result.get('error', 'کد تایید نادرست است')})
        
        return attrs
    
    def create(self, validated_data):
        # حذف otp_code از validated_data
        validated_data.pop('otp_code')
        phone_number = validated_data.pop('phone_number')
        
        # ایجاد کاربر
        user = User.objects.create_user(**validated_data)
        
        # ایجاد پروفایل (فقط اگر قبلاً وجود نداره)
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone_number': phone_number,
                'is_phone_verified': True
            }
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    """
    سریالایزر ورود با شماره موبایل و OTP
    """
    phone_number = serializers.CharField(max_length=11, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    
    def validate(self, attrs):
        phone_number = attrs['phone_number']
        otp_code = attrs['otp_code']
        
        # تایید کد OTP
        result = sms_service.verify_otp(phone_number, otp_code, 'login')
        
        if not result['success']:
            raise serializers.ValidationError({'otp_code': result.get('error', 'کد تایید نادرست است')})
        
        # بررسی وجود کاربر
        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
            attrs['user'] = profile.user
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({'phone_number': 'کاربری با این شماره موبایل یافت نشد'})
        
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    سریالایزر بازیابی رمز عبور
    """
    phone_number = serializers.CharField(max_length=11, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)
    
    def validate(self, attrs):
        phone_number = attrs['phone_number']
        otp_code = attrs['otp_code']
        
        # تایید کد OTP
        result = sms_service.verify_otp(phone_number, otp_code, 'password_reset')
        
        if not result['success']:
            raise serializers.ValidationError({'otp_code': result.get('error', 'کد تایید نادرست است')})
        
        # بررسی وجود کاربر
        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
            attrs['user'] = profile.user
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({'phone_number': 'کاربری با این شماره موبایل یافت نشد'})
        
        return attrs
    
    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class PurchaseNotificationSerializer(serializers.ModelSerializer):
    """
    سریالایزر اعلان خرید
    """
    class Meta:
        model = PurchaseNotification
        fields = ['id', 'order_id', 'amount', 'is_sent', 'sent_at', 'created_at']
        read_only_fields = ['id', 'is_sent', 'sent_at', 'created_at']

"""
سرویس ارسال پیامک
"""
import logging
import random
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# اگر Kavenegar نصب شد
try:
    from kavenegar import KavenegarAPI
    KAVENEGAR_AVAILABLE = True
except ImportError:
    KAVENEGAR_AVAILABLE = False
    logger.warning("Kavenegar not installed. SMS functionality will be limited.")


class SMSService:
    """سرویس ارسال پیامک"""
    
    def __init__(self):
        """مقداردهی اولیه"""
        self.api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
        self.sender = getattr(settings, 'KAVENEGAR_SENDER', '10004346')
        self.enabled = getattr(settings, 'SMS_ENABLED', False)
        
        if self.enabled and KAVENEGAR_AVAILABLE and self.api_key:
            try:
                self.api = KavenegarAPI(self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Kavenegar API: {str(e)}")
                self.api = None
        else:
            self.api = None
    
    def send_otp(self, mobile, code, template='verify'):
        """
        ارسال کد تأیید
        
        Args:
            mobile: شماره موبایل
            code: کد تأیید
            template: نام template در کاوه‌نگار
        
        Returns:
            bool: موفقیت یا عدم موفقیت
        """
        if not self.enabled:
            logger.info(f"SMS disabled. OTP code for {mobile}: {code}")
            return True
        
        if not self.api:
            logger.error("Kavenegar API not initialized")
            return False
        
        try:
            # ارسال با template
            params = {
                'receptor': mobile,
                'token': code,
                'template': template
            }
            
            response = self.api.verify_lookup(params)
            logger.info(f"OTP sent to {mobile}: {response}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send OTP to {mobile}: {str(e)}")
            return False
    
    def send_message(self, mobile, message):
        """
        ارسال پیام ساده
        
        Args:
            mobile: شماره موبایل
            message: متن پیام
        
        Returns:
            bool: موفقیت یا عدم موفقیت
        """
        if not self.enabled:
            logger.info(f"SMS disabled. Message for {mobile}: {message}")
            return True
        
        if not self.api:
            logger.error("Kavenegar API not initialized")
            return False
        
        try:
            params = {
                'sender': self.sender,
                'receptor': mobile,
                'message': message
            }
            
            response = self.api.sms_send(params)
            logger.info(f"SMS sent to {mobile}: {response}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send SMS to {mobile}: {str(e)}")
            return False
    
    def send_welcome_message(self, mobile, name):
        """ارسال پیام خوش‌آمدگویی"""
        message = f"سلام {name} عزیز، به VetLMS خوش آمدید! 🎉"
        return self.send_message(mobile, message)
    
    def send_payment_success(self, mobile, amount, ref_id):
        """ارسال پیام موفقیت پرداخت"""
        message = f"پرداخت {amount:,} تومانی شما با موفقیت انجام شد.\nشماره پیگیری: {ref_id}"
        return self.send_message(mobile, message)
    
    def send_subscription_activation(self, mobile, plan_name, expires_at):
        """ارسال پیام فعال‌سازی اشتراک"""
        message = f"اشتراک {plan_name} شما فعال شد.\nتاریخ انقضا: {expires_at}"
        return self.send_message(mobile, message)
    
    def send_subscription_expiry_warning(self, mobile, days_left):
        """ارسال هشدار انقضای اشتراک"""
        message = f"اشتراک شما {days_left} روز دیگر به پایان می‌رسد. برای تمدید اقدام کنید."
        return self.send_message(mobile, message)


class OTPManager:
    """مدیریت کدهای OTP"""
    
    OTP_EXPIRY = 120  # 2 دقیقه
    MAX_ATTEMPTS = 5
    
    @staticmethod
    def generate_otp():
        """تولید کد OTP 6 رقمی"""
        return str(random.randint(100000, 999999))
    
    @classmethod
    def create_and_send(cls, mobile, purpose='login'):
        """
        ایجاد و ارسال OTP
        
        Args:
            mobile: شماره موبایل
            purpose: هدف (login, register, reset_password)
        
        Returns:
            dict: {'success': bool, 'message': str, 'code': str (only in debug)}
        """
        # بررسی تعداد درخواست‌ها
        attempts_key = f'otp_attempts:{mobile}'
        attempts = cache.get(attempts_key, 0)
        
        if attempts >= cls.MAX_ATTEMPTS:
            return {
                'success': False,
                'message': 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً بعداً تلاش کنید.'
            }
        
        # تولید کد
        code = cls.generate_otp()
        
        # ذخیره در کش
        cache_key = f'otp:{mobile}:{purpose}'
        cache.set(cache_key, code, cls.OTP_EXPIRY)
        
        # افزایش تعداد تلاش‌ها
        cache.set(attempts_key, attempts + 1, 3600)  # 1 ساعت
        
        # ارسال پیامک
        sms_service = SMSService()
        success = sms_service.send_otp(mobile, code)
        
        if success:
            result = {
                'success': True,
                'message': f'کد تأیید به شماره {mobile} ارسال شد.'
            }
            # در حالت debug کد را برگردان
            if settings.DEBUG:
                result['code'] = code
            return result
        else:
            return {
                'success': False,
                'message': 'خطا در ارسال پیامک. لطفاً دوباره تلاش کنید.'
            }
    
    @classmethod
    def verify(cls, mobile, code, purpose='login'):
        """
        تأیید کد OTP
        
        Args:
            mobile: شماره موبایل
            code: کد وارد شده
            purpose: هدف
        
        Returns:
            bool: تأیید یا عدم تأیید
        """
        cache_key = f'otp:{mobile}:{purpose}'
        stored_code = cache.get(cache_key)
        
        if not stored_code:
            return False
        
        if stored_code == code:
            # حذف کد بعد از استفاده
            cache.delete(cache_key)
            return True
        
        return False


import random
from django.conf import settings
from django.core.cache import cache
from ippanel import Client
from ippanel import Error, HTTPError, ResponseCode

class FarazSMSService:
    """
    سرویس ارسال پیامک با استفاده از SDK رسمی فراز اس‌ام‌اس (IPPanel)
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'FARAZ_SMS_API_KEY', '')
        
        # شماره ارسال‌کننده (از پنل فراز اس‌ام‌اس)
        self.sender_number = getattr(settings, 'FARAZ_SMS_SENDER_NUMBER', '')
        
        # کدهای پترن از پنل فراز اس‌ام‌اس
        self.patterns = {
            'verification': getattr(settings, 'FARAZ_PATTERN_VERIFICATION', ''),
            'password_reset': getattr(settings, 'FARAZ_PATTERN_PASSWORD_RESET', ''),
            'purchase_success': getattr(settings, 'FARAZ_PATTERN_PURCHASE', ''),
            'login': getattr(settings, 'FARAZ_PATTERN_LOGIN', ''),
        }
        
        # ایجاد client instance
        try:
            self.client = Client(self.api_key)
        except Exception as e:
            print(f"Error initializing SMS client: {e}")
            self.client = None
    
    def generate_otp(self, length=6):
        """
        تولید کد OTP تصادفی
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def get_credit(self):
        """
        دریافت موجودی حساب
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'SMS client not initialized'}
            
            credit = self.client.get_credit()
            return {'success': True, 'credit': credit}
        except Error as e:
            return {'success': False, 'error': f"Code: {e.code}, Message: {e.message}"}
        except HTTPError as e:
            return {'success': False, 'error': f"HTTP Error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_sms(self, phone_number, message, summary=""):
        """
        ارسال پیامک ساده
        
        Args:
            phone_number: شماره موبایل گیرنده
            message: متن پیام
            summary: خلاصه پیام (اختیاری)
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'SMS client not initialized'}
            
            bulk_id = self.client.send(
                self.sender_number,  # sender
                [phone_number],      # recipients
                message,             # message
                summary              # summary (required in v2.x)
            )
            
            return {'success': True, 'bulk_id': bulk_id}
        except Error as e:
            return {'success': False, 'error': f"Code: {e.code}, Message: {e.message}"}
        except HTTPError as e:
            return {'success': False, 'error': f"HTTP Error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_pattern(self, phone_number, pattern_code, pattern_values):
        """
        ارسال پیامک با پترن
        
        Args:
            phone_number: شماره موبایل گیرنده
            pattern_code: کد پترن از پنل فراز اس‌ام‌اس
            pattern_values: دیکشنری مقادیر متغیرهای پترن
        
        Example:
            send_pattern(
                "09123456789",
                "abc123xyz",
                {"verification-code": "123456"}
            )
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'SMS client not initialized'}
            
            bulk_id = self.client.send_pattern(
                pattern_code,        # pattern code
                self.sender_number,  # originator
                phone_number,        # recipient
                pattern_values       # pattern values
            )
            
            return {'success': True, 'bulk_id': bulk_id}
        except Error as e:
            error_message = f"Code: {e.code}, Message: {e.message}"
            if e.code == ResponseCode.ErrUnprocessableEntity.value:
                # نمایش خطاهای فیلدها
                field_errors = []
                for field, errors in e.message.items():
                    field_errors.append(f"Field: {field}, Errors: {errors}")
                error_message += " | " + " | ".join(field_errors)
            return {'success': False, 'error': error_message}
        except HTTPError as e:
            return {'success': False, 'error': f"HTTP Error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_verification_code(self, phone_number, code):
        """
        ارسال کد تایید برای ثبت‌نام یا ورود
        """
        # استفاده از پترن در صورت وجود
        if self.patterns['verification']:
            return self.send_pattern(
                phone_number,
                self.patterns['verification'],
                {
                    'verification-code': code
                }
            )
        else:
            # ارسال پیامک ساده در صورت نبود پترن
            message = f"کد تایید شما: {code}\nاین کد به مدت 5 دقیقه معتبر است."
            return self.send_sms(phone_number, message)
    
    def send_password_reset_code(self, phone_number, code):
        """
        ارسال کد بازیابی رمز عبور
        """
        # استفاده از پترن در صورت وجود
        if self.patterns['password_reset']:
            return self.send_pattern(
                phone_number,
                self.patterns['password_reset'],
                {
                    'verification-code': code
                }
            )
        else:
            # ارسال پیامک ساده در صورت نبود پترن
            message = f"کد بازیابی رمز عبور: {code}\nاین کد به مدت 5 دقیقه معتبر است."
            return self.send_sms(phone_number, message)
    
    def send_login_code(self, phone_number, code):
        """
        ارسال کد ورود
        """
        # استفاده از پترن در صورت وجود
        if self.patterns['login']:
            return self.send_pattern(
                phone_number,
                self.patterns['login'],
                {
                    'verification-code': code
                }
            )
        else:
            # ارسال پیامک ساده در صورت نبود پترن
            message = f"کد ورود شما: {code}\nاین کد به مدت 5 دقیقه معتبر است."
            return self.send_sms(phone_number, message)
    
    def send_purchase_success(self, phone_number, order_id, amount):
        """
        ارسال پیام خرید موفق
        """
        # استفاده از پترن در صورت وجود
        if self.patterns['purchase_success']:
            return self.send_pattern(
                phone_number,
                self.patterns['purchase_success'],
                {
                    'order-id': order_id,
                    'amount': f'{amount:,}'
                }
            )
        else:
            # ارسال پیامک ساده در صورت نبود پترن
            message = f"خرید شما با موفقیت انجام شد.\nشماره سفارش: {order_id}\nمبلغ: {amount:,} تومان\nمتشکریم از خرید شما."
            return self.send_sms(phone_number, message)
    
    def send_otp_and_cache(self, phone_number, purpose='verification'):
        """
        تولید و ارسال کد OTP و ذخیره در کش
        purpose: 'verification', 'password_reset', 'login'
        """
        otp_code = self.generate_otp()
        
        # ذخیره در کش برای 5 دقیقه (300 ثانیه)
        cache_key = f'otp_{purpose}_{phone_number}'
        cache.set(cache_key, otp_code, 300)
        
        # ارسال پیامک بر اساس نوع
        if purpose == 'password_reset':
            result = self.send_password_reset_code(phone_number, otp_code)
        elif purpose == 'login':
            result = self.send_login_code(phone_number, otp_code)
        else:
            result = self.send_verification_code(phone_number, otp_code)
        
        if result['success']:
            return {'success': True, 'message': 'کد تایید با موفقیت ارسال شد', 'bulk_id': result.get('bulk_id')}
        else:
            return {'success': False, 'error': result.get('error', 'خطا در ارسال پیامک')}
    
    def verify_otp(self, phone_number, otp_code, purpose='verification'):
        """
        بررسی صحت کد OTP
        """
        cache_key = f'otp_{purpose}_{phone_number}'
        cached_otp = cache.get(cache_key)
        
        if not cached_otp:
            return {'success': False, 'error': 'کد تایید منقضی شده است'}
        
        if str(cached_otp) == str(otp_code):
            # حذف کد از کش بعد از تایید موفق
            cache.delete(cache_key)
            return {'success': True, 'message': 'کد تایید صحیح است'}
        else:
            return {'success': False, 'error': 'کد تایید نادرست است'}
    
    def get_message_status(self, bulk_id):
        """
        دریافت وضعیت پیام ارسال شده
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'SMS client not initialized'}
            
            message = self.client.get_message(bulk_id)
            
            return {
                'success': True,
                'status': message.status,
                'cost': message.cost,
                'payback': message.payback
            }
        except Error as e:
            return {'success': False, 'error': f"Code: {e.code}, Message: {e.message}"}
        except HTTPError as e:
            return {'success': False, 'error': f"HTTP Error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def fetch_delivery_statuses(self, bulk_id, page=0, page_size=10):
        """
        دریافت وضعیت تحویل پیام‌ها
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'SMS client not initialized'}
            
            statuses, pagination_info = self.client.fetch_statuses(bulk_id, page, page_size)
            
            status_list = []
            for status in statuses:
                status_list.append({
                    'recipient': status.recipient,
                    'status': status.status
                })
            
            return {
                'success': True,
                'statuses': status_list,
                'total': pagination_info.total
            }
        except Error as e:
            return {'success': False, 'error': f"Code: {e.code}, Message: {e.message}"}
        except HTTPError as e:
            return {'success': False, 'error': f"HTTP Error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def fetch_inbox(self, page=0, page_size=10):
        """
        دریافت پیام‌های دریافتی
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'SMS client not initialized'}
            
            messages, pagination_info = self.client.fetch_inbox(page, page_size)
            
            message_list = []
            for message in messages:
                message_list.append({
                    'message': message.message,
                    'sender': message.sender,
                    'number': message.number
                })
            
            return {
                'success': True,
                'messages': message_list,
                'total': pagination_info.total
            }
        except Error as e:
            return {'success': False, 'error': f"Code: {e.code}, Message: {e.message}"}
        except HTTPError as e:
            return {'success': False, 'error': f"HTTP Error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# نمونه استفاده
sms_service = FarazSMSService()
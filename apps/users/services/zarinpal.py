"""
سرویس زرین‌پال برای پرداخت آنلاین
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ZarinpalService:
    """سرویس زرین‌پال"""
    
    # URLs
    SANDBOX_REQUEST_URL = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
    SANDBOX_VERIFY_URL = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'
    SANDBOX_GATEWAY_URL = 'https://sandbox.zarinpal.com/pg/StartPay/'
    
    PRODUCTION_REQUEST_URL = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    PRODUCTION_VERIFY_URL = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
    PRODUCTION_GATEWAY_URL = 'https://www.zarinpal.com/pg/StartPay/'
    
    def __init__(self):
        """مقداردهی اولیه"""
        self.merchant_id = settings.ZARINPAL_MERCHANT_ID
        self.callback_url = settings.ZARINPAL_CALLBACK_URL
        self.sandbox = settings.ZARINPAL_SANDBOX_MODE
        
        # انتخاب URL های مناسب
        if self.sandbox:
            self.request_url = self.SANDBOX_REQUEST_URL
            self.verify_url = self.SANDBOX_VERIFY_URL
            self.gateway_url = self.SANDBOX_GATEWAY_URL
        else:
            self.request_url = self.PRODUCTION_REQUEST_URL
            self.verify_url = self.PRODUCTION_VERIFY_URL
            self.gateway_url = self.PRODUCTION_GATEWAY_URL
    
    def create_payment_request(self, amount, description, email=None, mobile=None):
        """
        ایجاد درخواست پرداخت با callback_url از تنظیمات
        
        Args:
            amount: مبلغ به تومان
            description: توضیحات پرداخت
            email: ایمیل (اختیاری)
            mobile: موبایل (اختیاری)
        
        Returns:
            tuple: (authority, payment_url) یا (None, error_message)
        """
        result = self.create_payment(
            amount=amount,
            description=description,
            callback_url=self.callback_url,
            email=email,
            mobile=mobile
        )
        
        if result['success']:
            return (result['authority'], result['url'])
        else:
            return (None, result['error'])
    
    def create_payment(self, amount, description, callback_url, email=None, mobile=None):
        """
        ایجاد درخواست پرداخت
        
        Args:
            amount: مبلغ به تومان
            description: توضیحات پرداخت
            callback_url: آدرس بازگشت
            email: ایمیل (اختیاری)
            mobile: موبایل (اختیاری)
        
        Returns:
            dict: {'success': bool, 'authority': str, 'url': str, 'error': str}
        """
        try:
            # داده‌های درخواست
            data = {
                'merchant_id': self.merchant_id,
                'amount': int(amount),
                'description': description,
                'callback_url': callback_url,
            }
            
            # اضافه کردن ایمیل و موبایل اگر وجود دارند
            if email:
                data['metadata'] = {'email': email}
            if mobile:
                data['metadata'] = data.get('metadata', {})
                data['metadata']['mobile'] = mobile
            
            # ارسال درخواست
            response = requests.post(
                self.request_url,
                json=data,
                timeout=10
            )
            
            result = response.json()
            
            # بررسی نتیجه
            if self.sandbox:
                # Sandbox
                if result.get('Status') == 100:
                    authority = result.get('Authority')
                    return {
                        'success': True,
                        'authority': authority,
                        'url': f"{self.gateway_url}{authority}",
                        'error': None
                    }
                else:
                    error_message = self._get_error_message(result.get('Status'))
                    logger.error(f"Zarinpal request error: {error_message}")
                    return {
                        'success': False,
                        'authority': None,
                        'url': None,
                        'error': error_message
                    }
            else:
                # Production
                if result.get('data', {}).get('code') == 100:
                    authority = result['data'].get('authority')
                    return {
                        'success': True,
                        'authority': authority,
                        'url': f"{self.gateway_url}{authority}",
                        'error': None
                    }
                else:
                    error_message = self._get_error_message(result.get('errors', {}).get('code'))
                    logger.error(f"Zarinpal request error: {error_message}")
                    return {
                        'success': False,
                        'authority': None,
                        'url': None,
                        'error': error_message
                    }
        
        except requests.exceptions.Timeout:
            logger.error("Zarinpal request timeout")
            return {
                'success': False,
                'authority': None,
                'url': None,
                'error': 'زمان درخواست به پایان رسید. لطفاً دوباره تلاش کنید.'
            }
        
        except Exception as e:
            logger.error(f"Zarinpal request exception: {str(e)}")
            return {
                'success': False,
                'authority': None,
                'url': None,
                'error': 'خطا در ارتباط با درگاه پرداخت'
            }
    
    def verify_payment(self, authority, amount):
        """
        تأیید پرداخت
        
        Args:
            authority: کد Authority
            amount: مبلغ به تومان
        
        Returns:
            tuple: (success, ref_id_or_error)
        """
        result = self._verify_payment_internal(authority, amount)
        if result['success']:
            return (True, result['ref_id'])
        else:
            return (False, result['error'])
    
    def _verify_payment_internal(self, authority, amount):
        """
        تأیید پرداخت - متد داخلی
        
        Args:
            authority: کد Authority
            amount: مبلغ به تومان
        
        Returns:
            dict: {'success': bool, 'ref_id': str, 'card_number': str, 'error': str}
        """
        try:
            # داده‌های درخواست
            data = {
                'merchant_id': self.merchant_id,
                'authority': authority,
                'amount': int(amount)
            }
            
            # ارسال درخواست
            response = requests.post(
                self.verify_url,
                json=data,
                timeout=10
            )
            
            result = response.json()
            
            # بررسی نتیجه
            if self.sandbox:
                # Sandbox
                if result.get('Status') == 100 or result.get('Status') == 101:
                    return {
                        'success': True,
                        'ref_id': str(result.get('RefID')),
                        'card_number': result.get('CardPan', ''),
                        'error': None
                    }
                else:
                    error_message = self._get_error_message(result.get('Status'))
                    logger.error(f"Zarinpal verify error: {error_message}")
                    return {
                        'success': False,
                        'ref_id': None,
                        'card_number': None,
                        'error': error_message
                    }
            else:
                # Production
                code = result.get('data', {}).get('code')
                if code == 100 or code == 101:
                    return {
                        'success': True,
                        'ref_id': str(result['data'].get('ref_id')),
                        'card_number': result['data'].get('card_pan', ''),
                        'error': None
                    }
                else:
                    error_message = self._get_error_message(result.get('errors', {}).get('code'))
                    logger.error(f"Zarinpal verify error: {error_message}")
                    return {
                        'success': False,
                        'ref_id': None,
                        'card_number': None,
                        'error': error_message
                    }
        
        except Exception as e:
            logger.error(f"Zarinpal verify exception: {str(e)}")
            return {
                'success': False,
                'ref_id': None,
                'card_number': None,
                'error': 'خطا در تأیید پرداخت'
            }
    
    def _get_error_message(self, code):
        """دریافت پیام خطا بر اساس کد"""
        error_messages = {
            -1: 'اطلاعات ارسال شده ناقص است',
            -2: 'IP یا مرچنت کد پذیرنده صحیح نیست',
            -3: 'مبلغ باید بیشتر از 1,000 تومان باشد',
            -4: 'سطح تأیید پذیرنده پایین‌تر از سطح نقره‌ای است',
            -11: 'درخواست مورد نظر یافت نشد',
            -12: 'امکان ویرایش درخواست میسر نمی‌باشد',
            -21: 'هیچ نوع عملیات مالی برای این تراکنش یافت نشد',
            -22: 'تراکنش ناموفق بوده است',
            -33: 'رقم تراکنش با رقم پرداخت شده مطابقت ندارد',
            -34: 'سقف تقسیم تراکنش از لحاظ تعداد یا مبلغ عبور کرده است',
            -40: 'اجازه دسترسی به متد مربوطه وجود ندارد',
            -41: 'اطلاعات ارسال شده مربوط به AdditionalData غیر معتبر است',
            -42: 'مدت زمان معتبر طول عمر شناسه پرداخت باید بین 30 دقیقه تا 45 روز باشد',
            -54: 'درخواست مورد نظر آرشیو شده است',
            100: 'عملیات موفق',
            101: 'عملیات پرداخت موفق - این تراکنش قبلاً ثبت شده',
        }
        return error_messages.get(code, f'خطای ناشناخته (کد: {code})')


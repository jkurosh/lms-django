"""
سرویس پرداخت با SDK زرین‌پال
"""

from django.conf import settings
from zarinpal import ZarinPal


class ZarinpalSDKService:
    """
    سرویس پرداخت با استفاده از SDK زرین‌پال
    """
    
    def __init__(self):
        self.merchant_id = getattr(settings, 'ZARINPAL_MERCHANT_ID', '')
        self.sandbox = getattr(settings, 'ZARINPAL_SANDBOX', False)
        
        # ایجاد client instance
        try:
            self.client = ZarinPal(merchant_id=self.merchant_id)
        except Exception as e:
            print(f"Error initializing Zarinpal client: {e}")
            self.client = None
    
    def create_payment(self, amount, callback_url, description, mobile=None, email=None):
        """
        ایجاد درخواست پرداخت
        
        Args:
            amount: مبلغ به ریال (حداقل 1000 ریال)
            callback_url: آدرس بازگشت بعد از پرداخت
            description: توضیحات تراکنش
            mobile: شماره موبایل پرداخت‌کننده (اختیاری)
            email: ایمیل پرداخت‌کننده (اختیاری)
        
        Returns:
            dict: شامل authority و payment_url در صورت موفقیت
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'Zarinpal client not initialized'}
            
            # ساخت دیتا
            payment_data = {
                'amount': amount,
                'description': description,
                'callback_url': callback_url
            }
            
            if mobile:
                payment_data['mobile'] = mobile
            if email:
                payment_data['email'] = email
            
            # ارسال درخواست
            response = self.client.request(payment_data)
            
            if response and 'authority' in response:
                authority = response['authority']
                payment_url = self.client.get_payment_link(authority)
                
                return {
                    'success': True,
                    'authority': authority,
                    'payment_url': payment_url,
                    'response': response
                }
            else:
                return {
                    'success': False,
                    'error': 'Authority not found in response',
                    'response': response
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def verify_payment(self, authority, amount):
        """
        تایید پرداخت
        
        Args:
            authority: کد authority دریافتی از زرین‌پال
            amount: مبلغ تراکنش (باید با مبلغ درخواست اولیه یکسان باشد)
        
        Returns:
            dict: شامل ref_id, card_pan در صورت موفقیت
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'Zarinpal client not initialized'}
            
            verify_data = {
                'amount': amount,
                'authority': authority
            }
            
            response = self.client.verify(verify_data)
            
            if response and 'ref_id' in response:
                return {
                    'success': True,
                    'verified': True,
                    'ref_id': response.get('ref_id'),
                    'card_pan': response.get('card_pan'),
                    'card_hash': response.get('card_hash'),
                    'fee_type': response.get('fee_type'),
                    'fee': response.get('fee'),
                    'message': 'پرداخت با موفقیت تایید شد'
                }
            else:
                return {
                    'success': False,
                    'verified': False,
                    'message': 'تایید پرداخت ناموفق بود',
                    'response': response
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_unverified_transactions(self):
        """
        دریافت تراکنش‌های تایید نشده
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'Zarinpal client not initialized'}
            
            response = self.client.un_verified()
            
            return {
                'success': True,
                'transactions': response
            }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


# نمونه استفاده
zarinpal_service = ZarinpalSDKService()
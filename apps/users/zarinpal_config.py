"""
پیکربندی زرین‌پال
"""
from django.conf import settings


class ZarinpalConfig:
    """
    کلاس پیکربندی زرین‌پال
    """
    def __init__(self):
        # دریافت تنظیمات از settings.py
        self.merchant_id = getattr(settings, 'ZARINPAL_MERCHANT_ID', '')
        self.access_token = getattr(settings, 'ZARINPAL_ACCESS_TOKEN', '')
        self.sandbox = getattr(settings, 'ZARINPAL_SANDBOX', True)
        
    def get_config_dict(self):
        """بازگشت تنظیمات به صورت دیکشنری"""
        return {
            'merchant_id': self.merchant_id,
            'access_token': self.access_token,
            'sandbox': self.sandbox,
        }


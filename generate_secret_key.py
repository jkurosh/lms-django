#!/usr/bin/env python
"""
اسکریپت برای تولید SECRET_KEY جدید برای Django
"""

from django.core.management.utils import get_random_secret_key

def generate_key():
    """تولید کلید مخفی جدید"""
    secret_key = get_random_secret_key()
    
    print("\n" + "="*60)
    print("🔑 SECRET_KEY جدید تولید شد")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("\n📝 نحوه استفاده:")
    print("   1. کپی کردن کلید بالا")
    print("   2. باز کردن فایل .env")
    print("   3. جایگزینی مقدار SECRET_KEY")
    print("\nمثال:")
    print(f"SECRET_KEY={secret_key}")
    print("\n⚠️  توجه:")
    print("   - این کلید را در جایی امن نگهداری کنید")
    print("   - هرگز این کلید را در Git commit نکنید")
    print("   - برای هر محیط (dev, staging, prod) کلید جداگانه")
    print("="*60 + "\n")

if __name__ == '__main__':
    generate_key()


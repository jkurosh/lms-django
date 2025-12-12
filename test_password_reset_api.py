#!/usr/bin/env python
"""
اسکریپت تست API فراموشی رمز عبور
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_verify_phone():
    """تست ارسال کد OTP"""
    url = f'{BASE_URL}/password-reset/verify-phone/'
    
    # شماره تست
    phone_number = '09385939627'
    
    data = {
        'phone_number': phone_number
    }
    
    print(f" تست ارسال کد به {phone_number}...")
    print(f"URL: {url}")
    print(f"Data: {data}")
    print("-" * 60)
    
    try:
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print("✅ موفق!")
        else:
            print("❌ خطا!")
            
    except requests.exceptions.ConnectionError:
        print("❌ خطا: سرور در دسترس نیست!")
        print("لطفاً مطمئن شوید که سرور در حال اجرا است:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"❌ خطا: {str(e)}")

def test_verify_otp():
    """تست تایید کد OTP"""
    url = f'{BASE_URL}/password-reset/verify-otp/'
    
    data = {
        'phone_number': '09123456789',
        'otp_code': '123456'
    }
    
    print(f"\n🧪 تست تایید کد OTP...")
    print(f"URL: {url}")
    print(f"Data: {data}")
    print("-" * 60)
    
    try:
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"❌ خطا: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 تست API فراموشی رمز عبور")
    print("=" * 60)
    
    test_verify_phone()
    # test_verify_otp()  # برای تست مرحله دوم
    
    print("\n" + "=" * 60)
    print("✅ تست تمام شد!")
    print("=" * 60)


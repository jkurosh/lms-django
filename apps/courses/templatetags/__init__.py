from django import template
from django.contrib.auth.models import User
from apps.courses.models import Case, CaseCategory, UserProgress

register = template.Library()

@register.simple_tag
def get_total_cases():
    """تعداد کل کیس‌ها"""
    try:
        return Case.objects.count()
    except:
        return 0

@register.simple_tag
def get_total_users():
    """تعداد کل کاربران"""
    try:
        return User.objects.count()
    except:
        return 0

@register.simple_tag
def get_total_categories():
    """تعداد کل دسته‌بندی‌ها"""
    try:
        return CaseCategory.objects.count()
    except:
        return 0

@register.simple_tag
def get_total_progress():
    """تعداد کل پیشرفت‌ها"""
    try:
        return UserProgress.objects.count()
    except:
        return 0

@register.simple_tag
def get_completed_cases():
    """تعداد کیس‌های تکمیل شده"""
    try:
        return UserProgress.objects.filter(completed=True).count()
    except:
        return 0

@register.simple_tag
def get_active_users():
    """تعداد کاربران فعال (با پیشرفت)"""
    try:
        return UserProgress.objects.values('user').distinct().count()
    except:
        return 0

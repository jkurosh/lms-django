from django import template
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from apps.courses.models import Case, CaseCategory, UserProgress, UserProfile

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

@register.simple_tag
def get_new_students_this_month():
    """تعداد دانشجویان جدید این ماه"""
    try:
        month_ago = timezone.now() - timedelta(days=30)
        return User.objects.filter(date_joined__gte=month_ago).count()
    except:
        return 0

@register.simple_tag
def get_monthly_completions():
    """تعداد تکمیل‌های این ماه"""
    try:
        month_ago = timezone.now() - timedelta(days=30)
        return UserProgress.objects.filter(
            completed=True,
            completed_at__gte=month_ago
        ).count()
    except:
        return 0

@register.simple_tag
def get_average_accuracy():
    """میانگین دقت کاربران"""
    try:
        profiles = UserProfile.objects.filter(total_observations__gt=0)
        if profiles.exists():
            return round(profiles.aggregate(avg=Avg('total_correct_observations') / Avg('total_observations') * 100)['avg'] or 0, 1)
        return 0
    except:
        return 0

@register.simple_tag
def get_category_stats():
    """آمار دسته‌بندی‌ها"""
    try:
        return CaseCategory.objects.annotate(
            case_count=Count('cases'),
            completed_count=Count('cases__user_progress', filter=Q(cases__user_progress__completed=True))
        ).order_by('-case_count')[:5]
    except:
        return []

@register.simple_tag
def get_recent_users():
    """کاربران اخیر با پیشرفت"""
    try:
        return User.objects.filter(
            case_progress__isnull=False
        ).distinct().order_by('-date_joined')[:5]
    except:
        return []

@register.filter
def mul(value, arg):
    """ضرب دو عدد"""
    try:
        return float(value) * float(arg)
    except:
        return 0

@register.filter
def div(value, arg):
    """تقسیم دو عدد"""
    try:
        if float(arg) != 0:
            return float(value) / float(arg)
        return 0
    except:
        return 0

@register.filter
def percentage(value, total):
    """محاسبه درصد"""
    try:
        if float(total) != 0:
            return round((float(value) / float(total)) * 100, 1)
        return 0
    except:
        return 0

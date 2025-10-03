from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from .models import CustomUser, Notification, Subscription
from .decorators import require_authentication, require_staff, rate_limit, secure_headers, subscription_required_or_admin
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from cases.models import Case, CaseCategory, SubCategory, Slide, UserProgress, UserProfile, UserObservation, Bookmark

def get_client_ip(request):
    """دریافت IP address کاربر"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_info(request):
    """دریافت اطلاعات دستگاه کاربر"""
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    return {
        'user_agent': user_agent,
        'timestamp': timezone.now().isoformat(),
        'ip': get_client_ip(request)
    }

def get_search_engine(request):
    """دریافت موتور جستجو از referer"""
    referer = request.META.get('HTTP_REFERER', '')
    if 'google' in referer.lower():
        return 'Google'
    elif 'bing' in referer.lower():
        return 'Bing'
    elif 'yahoo' in referer.lower():
        return 'Yahoo'
    elif 'duckduckgo' in referer.lower():
        return 'DuckDuckGo'
    else:
        return 'Direct'

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'dadash/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/designali/'
    
    def form_valid(self, form):
        """ثبت ورود موفق"""
        response = super().form_valid(form)
        
        # Record successful login
        ip_address = get_client_ip(self.request)
        device_info = get_device_info(self.request)
        self.request.user.record_successful_login(ip_address=ip_address, device_info=device_info)
        
        return response
    
    def form_invalid(self, form):
        """ثبت ورود ناموفق"""
        # Record failed login attempt
        username = form.cleaned_data.get('username')
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                ip_address = get_client_ip(self.request)
                user.record_failed_login(ip_address=ip_address)
            except CustomUser.DoesNotExist:
                pass
        
        return super().form_invalid(form)

@secure_headers
@rate_limit(max_requests=5, window_seconds=60)
@require_staff
def admin_panel(request):
    """پنل ادمین مدرن - فقط برای staff"""

    # دریافت آمار واقعی از دیتابیس
    from django.contrib.auth.models import User
    from cases.models import Case, CaseCategory, UserProgress, UserProfile
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # آمار کلی
        total_cases = Case.objects.count()
        total_users = User.objects.count()
        total_categories = CaseCategory.objects.count()
        completed_cases = UserProgress.objects.filter(completed=True).count()
        active_users = UserProgress.objects.values('user').distinct().count()
        
        # آمار ماهانه
        month_ago = timezone.now() - timedelta(days=30)
        new_students_this_month = User.objects.filter(date_joined__gte=month_ago).count()
        monthly_completions = UserProgress.objects.filter(
            completed=True,
            completed_at__gte=month_ago
        ).count()
        
        # آمار پیشرفت کاربران
        recent_progress = UserProgress.objects.select_related('user', 'case').order_by('-completed_at')[:10]
        
        # آمار دسته‌بندی‌ها با جزئیات بیشتر
        category_stats = []
        for category in CaseCategory.objects.all()[:5]:
            category_cases = category.cases.count()
            category_completed = UserProgress.objects.filter(
                case__category=category,
                completed=True
            ).count()
            category_stats.append({
                'name': category.name,
                'case_count': category_cases,
                'completed_count': category_completed,
                'completion_rate': round((category_completed / category_cases * 100) if category_cases > 0 else 0, 1)
            })
        
        # آمار کاربران فعال با جزئیات بیشتر
        user_stats = []
        for user in User.objects.filter(case_progress__isnull=False).distinct()[:5]:
            progress_count = UserProgress.objects.filter(user=user).count()
            completed_count = UserProgress.objects.filter(user=user, completed=True).count()
            try:
                profile = user.profile
                accuracy = profile.overall_accuracy
            except:
                accuracy = round((completed_count / progress_count * 100) if progress_count > 0 else 0, 1)
            
            user_stats.append({
                'name': user.get_full_name() or user.username,
                'username': user.username,
                'total_cases': progress_count,
                'completed_cases': completed_count,
                'accuracy': accuracy,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            })
        
        # آمار هفتگی (آخرین 7 روز)
        week_ago = timezone.now() - timedelta(days=7)
        weekly_completions = UserProgress.objects.filter(
            completed=True,
            completed_at__gte=week_ago
        ).count()
        
        # محاسبه درآمد تخمینی (بر اساس تکمیل کیس‌ها)
        estimated_income = completed_cases * 100  # 100 دلار به ازای هر کیس تکمیل شده
        
        # لیست اساتید (کاربران با دسترسی ادمین)
        professors = User.objects.filter(
            is_staff=True
        ).values('first_name', 'last_name', 'username', 'email', 'is_active')[:3]
        
        # لیست دانشجویان اخیر
        recent_students = User.objects.filter(
            case_progress__isnull=False
        ).distinct().order_by('-date_joined')[:4]
            
    except Exception as e:
        # در صورت خطا، از داده‌های پیش‌فرض استفاده کن
        print(f"خطا در دریافت آمار: {e}")
        total_cases = 0
        total_users = 0
        total_categories = 0
        completed_cases = 0
        active_users = 0
        new_students_this_month = 0
        monthly_completions = 0
        weekly_completions = 0
        estimated_income = 0
        recent_progress = []
        category_stats = []
        user_stats = []
        professors = []
        recent_students = []

    # داده‌های آماری
    context = {
        # آمار اصلی
        'total_cases': total_cases,
        'total_users': total_users,
        'total_categories': total_categories,
        'completed_cases': completed_cases,
        'active_users': active_users,
        
        # آمار ماهانه
        'new_students_this_month': new_students_this_month,
        'monthly_completions': monthly_completions,
        'weekly_completions': weekly_completions,
        
        # آمار تفصیلی
        'recent_progress': recent_progress,
        'category_stats': category_stats,
        'user_stats': user_stats,
        
        # داده‌های نمایشی (برای کارت‌های اصلی)
        'total_students': total_users,
        'new_students': new_students_this_month,
        'total_courses': total_categories,
        'total_income': estimated_income,
        
        # لیست‌های نمایشی
        'professors': professors,
        'recent_students': recent_students,
        
        # داده‌های نمایشی قدیمی (برای سازگاری)
        'students': [
            {'name': 'آنجلیکا راموس', 'coach': 'آشتون کاکس', 'date': '12 آگوست 2021', 'time': '10:15'},
            {'name': 'برادلی گریر', 'coach': 'برندن واگنر', 'date': '11 جولای 2021', 'time': '10:00'},
            {'name': 'سدریک کلی', 'coach': 'بریل ویلیامسون', 'date': '10 می 2021', 'time': '09:45'},
            {'name': 'سزار ونس', 'coach': 'هرود چندلر', 'date': '09 آوریل 2021', 'time': '08:30'},
        ]
    }

    return render(request, 'dadash/admin_panel.html', context)

def register_view(request):
    """صفحه ثبت‌نام"""
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.')
            return render(request, 'dadash/register.html')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً استفاده شده است.')
            return render(request, 'dadash/register.html')
        
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'این شماره تلفن قبلاً استفاده شده است.')
            return render(request, 'dadash/register.html')
        
        # Get IP address
        ip_address = get_client_ip(request)
        
        # Get device info
        device_info = get_device_info(request)
        
        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            phone_number=phone_number,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            ip_address=ip_address,
            search_engine=get_search_engine(request)
        )
        
        # Add device to user's devices list
        if device_info:
            user.devices = [device_info]
            user.save()
        
        # Create user profile
        # UserProfile.objects.create(user=user)  # Temporarily disabled - table doesn't exist
        
        # Login user and record successful login
        login(request, user)
        user.record_successful_login(ip_address=ip_address, device_info=device_info)
        
        messages.success(request, f'حساب کاربری {username} با موفقیت ایجاد شد!')
        return redirect('heyvoonak:designali_dashboard')
    
    return render(request, 'dadash/register.html')

def logout_view(request):
    """خروج از سیستم"""
    logout(request)
    messages.success(request, 'با موفقیت از سیستم خارج شدید.')
    return redirect('heyvoonak:landing_page')

def dadash_home(request):
    """صفحه اصلی heyvoonak - لندینگ پیج"""
    return render(request, 'dadash/landing.html')

def categories_home(request):
    """صفحه اصلی کتگوری‌ها"""
    categories = CaseCategory.objects.annotate(case_count=Count('cases'))
    
    context = {
        'categories': categories,
        'total_cases': Case.objects.count(),
    }
    return render(request, 'dadash/index.html', context)

def internal_diseases(request):
    """صفحه بیماری‌های داخلی"""
    cases = Case.objects.filter(category__name__icontains='داخلی').prefetch_related('slides')
    
    context = {
        'cases': cases,
        'category_name': 'بیماری‌های داخلی',
    }
    return render(request, 'dadash/internal-diseases.html', context)

def surgery(request):
    """صفحه جراحی"""
    cases = Case.objects.filter(category__name__icontains='جراحی').prefetch_related('slides')
    
    context = {
        'cases': cases,
        'category_name': 'جراحی',
    }
    return render(request, 'dadash/surgery.html', context)

def emergency(request):
    """صفحه اورژانس"""
    cases = Case.objects.filter(category__name__icontains='اورژانس').prefetch_related('slides')
    
    context = {
        'cases': cases,
        'category_name': 'پزشکی اورژانس',
    }
    return render(request, 'dadash/emergency.html', context)

def dermatology(request):
    """صفحه پوست‌شناسی"""
    cases = Case.objects.filter(category__name__icontains='پوست').prefetch_related('slides')
    
    context = {
        'cases': cases,
        'category_name': 'پوست‌شناسی',
    }
    return render(request, 'dadash/dermatology.html', context)

def radiology(request):
    """صفحه رادیولوژی"""
    cases = Case.objects.filter(category__name__icontains='رادیولوژی').prefetch_related('slides')
    
    context = {
        'cases': cases,
        'category_name': 'رادیولوژی',
    }
    return render(request, 'dadash/radiology.html', context)

def cardiology(request):
    """صفحه قلب‌شناسی"""
    cases = Case.objects.filter(category__name__icontains='قلب').prefetch_related('slides')
    
    context = {
        'cases': cases,
        'category_name': 'قلب‌شناسی',
    }
    return render(request, 'dadash/cardiology.html', context)

def landing_page(request):
    """لندینگ پیج جدید BBros"""
    return render(request, 'dadash/landing.html')

def get_subcategories_api(request, category_id):
    """API برای دریافت subcategories یک دسته‌بندی"""
    try:
        from django.db.models import Count
        
        # دریافت subcategories برای دسته‌بندی مشخص
        subcategories = SubCategory.objects.filter(
            category_id=category_id
        ).annotate(
            case_count=Count('cases')
        ).values(
            'id', 'name', 'description', 'case_count'
        ).order_by('name')
        
        return JsonResponse({
            'success': True,
            'subcategories': list(subcategories)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def toggle_bookmark_api(request, case_id):
    """API برای bookmark/unbookmark کردن یک case"""
    try:
        case = Case.objects.get(id=case_id)
        user = request.user
        
        # بررسی وجود bookmark
        bookmark, created = Bookmark.objects.get_or_create(
            user=user,
            case=case
        )
        
        if created:
            # Bookmark اضافه شد
            return JsonResponse({
                'success': True,
                'action': 'bookmarked',
                'message': 'Case bookmark شد'
            })
        else:
            # Bookmark حذف شد
            bookmark.delete()
            return JsonResponse({
                'success': True,
                'action': 'unbookmarked',
                'message': 'Case از bookmark حذف شد'
            })
            
    except Case.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Case یافت نشد'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def get_bookmarks_api(request):
    """API برای دریافت bookmark های کاربر"""
    try:
        bookmarks = Bookmark.objects.filter(
            user=request.user
        ).select_related('case', 'case__category').values(
            'id', 'created_at', 'notes',
            'case__id', 'case__title', 'case__description',
            'case__category__name'
        ).order_by('-created_at')
        
        return JsonResponse({
            'success': True,
            'bookmarks': list(bookmarks)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def check_bookmark_status_api(request, case_id):
    """API برای بررسی وضعیت bookmark یک case"""
    try:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user,
            case_id=case_id
        ).exists()
        
        return JsonResponse({
            'success': True,
            'is_bookmarked': is_bookmarked
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def remove_bookmark_api(request, bookmark_id):
    """API برای حذف bookmark"""
    try:
        bookmark = Bookmark.objects.get(id=bookmark_id, user=request.user)
        bookmark.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Bookmark حذف شد'
        })
    except Bookmark.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Bookmark یافت نشد'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def categories_page(request):
    """صفحه کتگوری‌ها و ساب کتگوری‌ها - نسخه با دیتابیس واقعی"""
    from django.core.paginator import Paginator
    from django.db.models import Count
    
    # دریافت پارامترهای فیلتر
    selected_category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    page_number = int(request.GET.get('page', 1))
    
    try:
        # دریافت همه کتگوری‌ها از دیتابیس
        categories = CaseCategory.objects.annotate(
            subcategory_count=Count('subcategories')
        ).order_by('name')
        
        # فیلتر ساب کتگوری‌ها
        subcategories_query = SubCategory.objects.annotate(
            case_count=Count('cases')
        ).select_related('category')
        
        # فیلتر بر اساس کتگوری انتخاب شده
        if selected_category != 'all':
            try:
                category_id = int(selected_category)
                subcategories_query = subcategories_query.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        
        # فیلتر بر اساس جستجو
        if search_query:
            subcategories_query = subcategories_query.filter(
                name__icontains=search_query
            )
        
        # مرتب‌سازی
        subcategories_query = subcategories_query.order_by('name')
        
        # صفحه‌بندی
        paginator = Paginator(subcategories_query, 30)  # 30 آیتم در هر صفحه
        subcategories = paginator.get_page(page_number)
        
        current_page = subcategories.number
        total_pages = paginator.num_pages
        
    except Exception as e:
        # در صورت خطا، داده‌های نمونه نمایش دهیم
        print(f"خطا در دریافت داده‌ها از دیتابیس: {e}")
        
        # داده‌های نمونه
        categories = [
            {'id': 1, 'name': 'بیماری‌های داخلی', 'subcategory_count': 5},
            {'id': 2, 'name': 'جراحی', 'subcategory_count': 3},
            {'id': 3, 'name': 'اورژانس', 'subcategory_count': 4},
            {'id': 4, 'name': 'پوست‌شناسی', 'subcategory_count': 2},
            {'id': 5, 'name': 'رادیولوژی', 'subcategory_count': 3},
            {'id': 6, 'name': 'قلب‌شناسی', 'subcategory_count': 4},
            {'id': 7, 'name': 'عصب‌شناسی', 'subcategory_count': 3},
            {'id': 8, 'name': 'چشم‌پزشکی', 'subcategory_count': 2},
        ]
        
        subcategories_data = [
            {'id': 1, 'name': 'بیماری‌های گوارشی', 'description': 'مطالعات موردی مربوط به بیماری‌های دستگاه گوارش شامل التهاب معده، زخم معده، انسداد روده و سایر مشکلات گوارشی', 'case_count': 15, 'category': {'name': 'بیماری‌های داخلی'}},
            {'id': 2, 'name': 'بیماری‌های قلبی', 'description': 'مطالعات موردی مربوط به بیماری‌های قلبی و عروقی شامل نارسایی قلبی، آریتمی و بیماری‌های دریچه‌ای', 'case_count': 12, 'category': {'name': 'بیماری‌های داخلی'}},
            {'id': 3, 'name': 'بیماری‌های کلیوی', 'description': 'مطالعات موردی مربوط به بیماری‌های کلیه و مجاری ادراری', 'case_count': 8, 'category': {'name': 'بیماری‌های داخلی'}},
            {'id': 4, 'name': 'بیماری‌های کبدی', 'description': 'مطالعات موردی مربوط به بیماری‌های کبد و مجاری صفراوی', 'case_count': 10, 'category': {'name': 'بیماری‌های داخلی'}},
            {'id': 5, 'name': 'بیماری‌های تنفسی', 'description': 'مطالعات موردی مربوط به بیماری‌های دستگاه تنفسی', 'case_count': 9, 'category': {'name': 'بیماری‌های داخلی'}},
            
            {'id': 6, 'name': 'جراحی عمومی', 'description': 'مطالعات موردی جراحی‌های عمومی شامل لاپاراسکوپی و جراحی‌های باز', 'case_count': 8, 'category': {'name': 'جراحی'}},
            {'id': 7, 'name': 'جراحی ارتوپدی', 'description': 'مطالعات موردی جراحی‌های استخوان و مفاصل', 'case_count': 10, 'category': {'name': 'جراحی'}},
            {'id': 8, 'name': 'جراحی نرم', 'description': 'مطالعات موردی جراحی‌های بافت نرم', 'case_count': 6, 'category': {'name': 'جراحی'}},
            
            {'id': 9, 'name': 'تروما', 'description': 'مطالعات موردی آسیب‌های ناشی از ضربه و تصادف', 'case_count': 20, 'category': {'name': 'اورژانس'}},
            {'id': 10, 'name': 'مسمومیت', 'description': 'مطالعات موردی مسمومیت‌ها و مسمومیت‌های غذایی', 'case_count': 7, 'category': {'name': 'اورژانس'}},
            {'id': 11, 'name': 'شوک', 'description': 'مطالعات موردی انواع شوک و مدیریت آن', 'case_count': 5, 'category': {'name': 'اورژانس'}},
            {'id': 12, 'name': 'تنفس مصنوعی', 'description': 'مطالعات موردی مدیریت تنفس مصنوعی', 'case_count': 4, 'category': {'name': 'اورژانس'}},
            
            {'id': 13, 'name': 'درماتیت', 'description': 'مطالعات موردی التهاب‌های پوستی و آلرژی', 'case_count': 6, 'category': {'name': 'پوست‌شناسی'}},
            {'id': 14, 'name': 'عفونت‌های پوستی', 'description': 'مطالعات موردی عفونت‌های باکتریایی و قارچی پوست', 'case_count': 4, 'category': {'name': 'پوست‌شناسی'}},
            
            {'id': 15, 'name': 'رادیولوژی تشخیصی', 'description': 'مطالعات موردی تصویربرداری تشخیصی شامل X-ray و CT', 'case_count': 14, 'category': {'name': 'رادیولوژی'}},
            {'id': 16, 'name': 'سونوگرافی', 'description': 'مطالعات موردی سونوگرافی و تشخیص‌های اولتراسوند', 'case_count': 8, 'category': {'name': 'رادیولوژی'}},
            {'id': 17, 'name': 'MRI', 'description': 'مطالعات موردی تصویربرداری MRI', 'case_count': 3, 'category': {'name': 'رادیولوژی'}},
            
            {'id': 18, 'name': 'نارسایی قلبی', 'description': 'مطالعات موردی نارسایی قلبی و مدیریت آن', 'case_count': 6, 'category': {'name': 'قلب‌شناسی'}},
            {'id': 19, 'name': 'آریتمی', 'description': 'مطالعات موردی آریتمی‌های قلبی', 'case_count': 4, 'category': {'name': 'قلب‌شناسی'}},
            {'id': 20, 'name': 'بیماری‌های دریچه‌ای', 'description': 'مطالعات موردی بیماری‌های دریچه‌های قلبی', 'case_count': 3, 'category': {'name': 'قلب‌شناسی'}},
            {'id': 21, 'name': 'کاردیومیوپاتی', 'description': 'مطالعات موردی کاردیومیوپاتی و بیماری‌های عضله قلب', 'case_count': 2, 'category': {'name': 'قلب‌شناسی'}},
            
            {'id': 22, 'name': 'صرع', 'description': 'مطالعات موردی صرع و تشنج', 'case_count': 5, 'category': {'name': 'عصب‌شناسی'}},
            {'id': 23, 'name': 'سکته مغزی', 'description': 'مطالعات موردی سکته مغزی و عوارض آن', 'case_count': 3, 'category': {'name': 'عصب‌شناسی'}},
            {'id': 24, 'name': 'بیماری‌های عصبی', 'description': 'مطالعات موردی بیماری‌های عصبی مزمن', 'case_count': 4, 'category': {'name': 'عصب‌شناسی'}},
            
            {'id': 25, 'name': 'بیماری‌های چشم', 'description': 'مطالعات موردی بیماری‌های چشم و بینایی', 'case_count': 3, 'category': {'name': 'چشم‌پزشکی'}},
            {'id': 26, 'name': 'جراحی چشم', 'description': 'مطالعات موردی جراحی‌های چشم', 'case_count': 2, 'category': {'name': 'چشم‌پزشکی'}},
        ]
        
        # فیلتر داده‌های نمونه
        if selected_category != 'all':
            try:
                category_id = int(selected_category)
                category_name = next((cat['name'] for cat in categories if cat['id'] == category_id), None)
                if category_name:
                    subcategories_data = [sc for sc in subcategories_data if sc['category']['name'] == category_name]
            except (ValueError, TypeError):
                pass
        
        if search_query:
            subcategories_data = [sc for sc in subcategories_data if search_query.lower() in sc['name'].lower()]
        
        # صفحه‌بندی دستی
        items_per_page = 30
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_subcategories = subcategories_data[start_index:end_index]
        
        # ایجاد object شبیه‌سازی شده برای صفحه‌بندی
        class MockPage:
            def __init__(self, items, number, total_pages):
                self.object_list = items
                self.number = number
                self.total_pages = total_pages
        
        total_pages = (len(subcategories_data) + items_per_page - 1) // items_per_page
        subcategories = MockPage(paginated_subcategories, page_number, total_pages)
        current_page = page_number
    
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': selected_category,
        'search_query': search_query,
        'current_page': current_page,
        'total_pages': total_pages,
    }
    
    return render(request, 'dadash/categories.html', context)

@secure_headers
@rate_limit(max_requests=10, window_seconds=60)
@require_authentication
def designali_dashboard(request):
    """داشبورد Designali Creative - نیاز به ورود"""
    
    user = request.user
    
    # دریافت bookmark های کاربر
    user_bookmarks = []
    if user.is_authenticated:
        user_bookmarks = Bookmark.objects.filter(user=user).select_related('case', 'case__category').order_by('-created_at')[:5]
    
    # دریافت آخرین مطالعات موردی از دیتابیس
    recent_cases = Case.objects.select_related('category').order_by('-created_at')[:5]
    
    # محاسبه آمار واقعی
    total_cases = Case.objects.count()
    completed_cases = UserProgress.objects.filter(completed=True).count()
    in_progress_cases = UserProgress.objects.filter(completed=False).count()
    
    # محاسبه درصد تکمیل
    completion_percentage = 0
    if total_cases > 0:
        completion_percentage = round((completed_cases / total_cases) * 100, 1)
    
    # دریافت محبوب‌ترین دسته‌بندی‌ها
    from django.db.models import Count
    popular_categories = CaseCategory.objects.annotate(
        case_count=Count('cases')
    ).order_by('-case_count')[:5]
    
    context = {
        'profile': {
            'overall_accuracy': 85.5,
            'total_cases_completed': completed_cases,
        },
        'total_cases': total_cases,
        'completed_cases': completed_cases,
        'in_progress_cases': in_progress_cases,
        'user_bookmarks': user_bookmarks,
        'recent_cases': recent_cases,
        'popular_categories': popular_categories,
        'weekly_progress': 5,
        'monthly_progress': 18,
        'completion_percentage': completion_percentage,
    }
    
    return render(request, 'dadash/designali_dashboard.html', context)

@login_required
def dashboard(request):
    """داشبورد اصلی کاربر"""
    user = request.user
    
    # دریافت یا ایجاد پروفایل کاربر
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # آمار کلی
    total_cases = Case.objects.count()
    completed_cases = UserProgress.objects.filter(user=user, completed=True).count()
    in_progress_cases = UserProgress.objects.filter(user=user, completed=False).count()
    
    # آمار اخیر
    recent_progress = UserProgress.objects.filter(user=user).order_by('-updated_at')[:5]
    
    # کیس‌های اخیر
    recent_cases = Case.objects.filter(is_published=True).order_by('-created_at')[:6]
    
    # دسته‌بندی‌های محبوب
    popular_categories = CaseCategory.objects.annotate(
        case_count=Count('cases'),
        user_progress_count=Count('cases__user_progress', filter=Q(cases__user_progress__user=user))
    ).order_by('-case_count')[:6]
    
    # آمار هفتگی
    week_ago = timezone.now() - timedelta(days=7)
    weekly_progress = UserProgress.objects.filter(
        user=user,
        updated_at__gte=week_ago
    ).count()
    
    # آمار ماهانه
    month_ago = timezone.now() - timedelta(days=30)
    monthly_progress = UserProgress.objects.filter(
        user=user,
        updated_at__gte=month_ago
    ).count()
    
    context = {
        'profile': profile,
        'total_cases': total_cases,
        'completed_cases': completed_cases,
        'in_progress_cases': in_progress_cases,
        'recent_progress': recent_progress,
        'recent_cases': recent_cases,
        'popular_categories': popular_categories,
        'weekly_progress': weekly_progress,
        'monthly_progress': monthly_progress,
        'completion_percentage': round((completed_cases / total_cases * 100) if total_cases > 0 else 0, 1),
    }
    
    return render(request, 'dadash/dashboard.html', context)

@login_required
def my_cases(request):
    """کیس‌های کاربر"""
    user = request.user
    status_filter = request.GET.get('status', 'all')
    category_filter = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    
    # فیلتر کیس‌ها
    cases_query = Case.objects.filter(is_published=True)
    
    if search_query:
        cases_query = cases_query.filter(
            Q(title__icontains=search_query) | 
            Q(summary__icontains=search_query)
        )
    
    if category_filter != 'all':
        cases_query = cases_query.filter(category_id=category_filter)
    
    # دریافت پیشرفت کاربر برای هر کیس
    user_cases = []
    for case in cases_query:
        progress = UserProgress.objects.filter(user=user, case=case).first()
        user_cases.append({
            'case': case,
            'progress': progress,
            'is_completed': progress.completed if progress else False,
            'score': progress.score if progress else None,
            'attempts': progress.attempts if progress else 0,
        })
    
    # فیلتر بر اساس وضعیت
    if status_filter == 'completed':
        user_cases = [uc for uc in user_cases if uc['is_completed']]
    elif status_filter == 'in_progress':
        user_cases = [uc for uc in user_cases if not uc['is_completed'] and uc['attempts'] > 0]
    elif status_filter == 'not_started':
        user_cases = [uc for uc in user_cases if uc['attempts'] == 0]
    
    # دسته‌بندی‌ها برای فیلتر
    categories = CaseCategory.objects.annotate(case_count=Count('cases')).order_by('name')
    
    context = {
        'user_cases': user_cases,
        'categories': categories,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    
    return render(request, 'dadash/my_cases.html', context)

@login_required
def analytics(request):
    """صفحه آمار و تحلیل"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # آمار کلی
    total_progress = UserProgress.objects.filter(user=user)
    completed_progress = total_progress.filter(completed=True)
    
    # آمار دسته‌بندی‌ها
    category_stats = []
    categories = CaseCategory.objects.all()
    for category in categories:
        category_cases = Case.objects.filter(category=category, is_published=True)
        user_category_progress = UserProgress.objects.filter(
            user=user, 
            case__in=category_cases
        )
        completed_in_category = user_category_progress.filter(completed=True).count()
        
        category_stats.append({
            'category': category,
            'total_cases': category_cases.count(),
            'completed': completed_in_category,
            'completion_rate': round((completed_in_category / category_cases.count() * 100) if category_cases.count() > 0 else 0, 1),
        })
    
    # آمار ماهانه (آخرین 12 ماه)
    monthly_stats = []
    for i in range(12):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        
        monthly_completed = UserProgress.objects.filter(
            user=user,
            completed=True,
            completed_at__gte=month_start,
            completed_at__lt=month_end
        ).count()
        
        monthly_stats.append({
            'month': month_start.strftime('%Y-%m'),
            'completed': monthly_completed,
        })
    
    monthly_stats.reverse()
    
    # آمار هفتگی (آخرین 8 هفته)
    weekly_stats = []
    for i in range(8):
        week_start = timezone.now() - timedelta(days=7*(i+1))
        week_end = timezone.now() - timedelta(days=7*i)
        
        weekly_completed = UserProgress.objects.filter(
            user=user,
            completed=True,
            completed_at__gte=week_start,
            completed_at__lt=week_end
        ).count()
        
        weekly_stats.append({
            'week': f'هفته {8-i}',
            'completed': weekly_completed,
        })
    
    weekly_stats.reverse()
    
    context = {
        'profile': profile,
        'total_progress': total_progress.count(),
        'completed_progress': completed_progress.count(),
        'category_stats': category_stats,
        'monthly_stats': monthly_stats,
        'weekly_stats': weekly_stats,
    }
    
    return render(request, 'dadash/analytics.html', context)

@login_required
def achievements(request):
    """صفحه دستاوردها"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # محاسبه دستاوردها
    achievements = []
    
    # دستاوردهای کلی
    total_completed = UserProgress.objects.filter(user=user, completed=True).count()
    
    if total_completed >= 1:
        achievements.append({
            'title': 'شروع کننده',
            'description': 'اولین کیس خود را تکمیل کردید',
            'icon': '🎯',
            'earned': True,
            'date': UserProgress.objects.filter(user=user, completed=True).first().completed_at,
        })
    
    if total_completed >= 5:
        achievements.append({
            'title': 'متعلم',
            'description': '5 کیس را تکمیل کردید',
            'icon': '📚',
            'earned': True,
            'date': UserProgress.objects.filter(user=user, completed=True)[4].completed_at,
        })
    
    if total_completed >= 10:
        achievements.append({
            'title': 'متخصص',
            'description': '10 کیس را تکمیل کردید',
            'icon': '🏆',
            'earned': True,
            'date': UserProgress.objects.filter(user=user, completed=True)[9].completed_at,
        })
    
    if total_completed >= 25:
        achievements.append({
            'title': 'استاد',
            'description': '25 کیس را تکمیل کردید',
            'icon': '👑',
            'earned': True,
            'date': UserProgress.objects.filter(user=user, completed=True)[24].completed_at,
        })
    
    # دستاوردهای دقت
    if profile.overall_accuracy >= 80:
        achievements.append({
            'title': 'دقیق',
            'description': 'دقت کلی بالای 80%',
            'icon': '🎯',
            'earned': True,
            'date': None,
        })
    
    if profile.overall_accuracy >= 90:
        achievements.append({
            'title': 'نابغه',
            'description': 'دقت کلی بالای 90%',
            'icon': '🧠',
            'earned': True,
            'date': None,
        })
    
    # دستاوردهای دسته‌بندی
    categories = CaseCategory.objects.all()
    for category in categories:
        category_cases = Case.objects.filter(category=category, is_published=True)
        completed_in_category = UserProgress.objects.filter(
            user=user,
            case__in=category_cases,
            completed=True
        ).count()
        
        if completed_in_category >= category_cases.count() and category_cases.count() > 0:
            achievements.append({
                'title': f'متخصص {category.name}',
                'description': f'همه کیس‌های {category.name} را تکمیل کردید',
                'icon': '🏅',
                'earned': True,
                'date': None,
            })
    
    # دستاوردهای آینده (هنوز کسب نشده)
    if total_completed < 50:
        achievements.append({
            'title': 'قهرمان',
            'description': '50 کیس را تکمیل کنید',
            'icon': '🥇',
            'earned': False,
            'progress': total_completed,
            'target': 50,
        })
    
    if profile.overall_accuracy < 95:
        achievements.append({
            'title': 'کمال‌گرا',
            'description': 'دقت کلی بالای 95%',
            'icon': '💎',
            'earned': False,
            'progress': profile.overall_accuracy,
            'target': 95,
        })
    
    context = {
        'profile': profile,
        'achievements': achievements,
        'total_achievements': len([a for a in achievements if a['earned']]),
        'total_possible': len(achievements),
    }
    
    return render(request, 'dadash/achievements.html', context)

@login_required
def profile_settings(request):
    """تنظیمات پروفایل کاربر"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # به‌روزرسانی اطلاعات کاربر
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        messages.success(request, 'اطلاعات پروفایل با موفقیت به‌روزرسانی شد.')
        return redirect('heyvoonak:profile_settings')
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'dadash/profile_settings.html', context)


@secure_headers
@rate_limit(max_requests=3, window_seconds=60)
@require_staff
def send_notification_view(request):
    """ارسال اعلان جدید"""
    
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            title = data.get('title')
            message = data.get('message')
            notification_type = data.get('notification_type', 'info')
            is_broadcast = data.get('is_broadcast', True)
            expires_at = data.get('expires_at')
            
            if not title or not message:
                return JsonResponse({'success': False, 'message': 'عنوان و پیام الزامی است'})
            
            # Parse expiry date if provided
            expiry_date = None
            if expires_at:
                try:
                    expiry_date = timezone.datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                except:
                    pass
            
            print(f"Debug - is_broadcast: {is_broadcast}, type: {type(is_broadcast)}")
            
            if is_broadcast:
                # ارسال به همه کاربران فعال
                users = CustomUser.objects.filter(is_active=True)
                notification_count = 0
                
                for user in users:
                    Notification.objects.create(
                        title=title,
                        message=message,
                        notification_type=notification_type,
                        recipient=user,
                        sender=request.user,
                        expires_at=expiry_date,
                        is_broadcast=True
                    )
                    notification_count += 1
                
                return JsonResponse({
                    'success': True, 
                    'message': f'اعلان برای {notification_count} کاربر ارسال شد'
                })
            else:
                # ارسال به کاربر خاص (در آینده پیاده‌سازی شود)
                return JsonResponse({
                    'success': False, 
                    'message': 'ارسال به کاربر خاص هنوز پیاده‌سازی نشده است'
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'روش درخواست نامعتبر'})


def get_notifications_stats(request):
    """دریافت آمار اعلان‌ها"""
    # بررسی لاگین بودن کاربر
    if not request.user.is_authenticated:
        return JsonResponse({'total': 0, 'unread': 0}, status=401)
    
    try:
        total_notifications = Notification.objects.count()
        unread_notifications = Notification.objects.filter(is_read=False, is_active=True).count()
        
        return JsonResponse({
            'total': total_notifications,
            'unread': unread_notifications
        })
    except Exception as e:
        return JsonResponse({'total': 0, 'unread': 0})


@login_required
def user_notifications_view(request):
    """دریافت اعلان‌های کاربر"""
    try:
        notifications = Notification.objects.filter(
            recipient=request.user,
            is_active=True
        ).exclude(
            expires_at__lt=timezone.now()
        ).order_by('-created_at')[:20]
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'notification_type': notification.notification_type,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),
                'sender': notification.sender.get_full_name() if notification.sender else None
            })
        
        return JsonResponse({
            'notifications': notifications_data,
            'unread_count': notifications.filter(is_read=False).count()
        })
    except Exception as e:
        return JsonResponse({'notifications': [], 'unread_count': 0})


@login_required
def mark_notification_read_view(request, notification_id):
    """علامت‌گذاری اعلان به عنوان خوانده شده"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.mark_as_read()
        
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'اعلان یافت نشد'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def mark_all_notifications_read_view(request):
    """علامت‌گذاری همه اعلان‌ها به عنوان خوانده شده"""
    try:
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def delete_notification_view(request, notification_id):
    """حذف اعلان"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.delete()
        
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'اعلان یافت نشد'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def subscription_status(request):
    """نمایش وضعیت اشتراک کاربر"""
    try:
        subscription = request.user.subscription
        context = {
            'subscription': subscription,
            'is_active': subscription.is_active(),
            'days_remaining': subscription.days_remaining(),
        }
    except Subscription.DoesNotExist:
        context = {
            'subscription': None,
            'is_active': False,
            'days_remaining': 0,
        }
    
    return render(request, 'dadash/subscription_status.html', context)

def security_warning(request):
    """صفحه هشدار امنیتی"""
    return render(request, 'dadash/security_warning.html')
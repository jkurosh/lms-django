from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    Case,
    LabTest,
    UserProgress,
    UserObservation,
    UserProfile,
    CaseCategory,
    CBC_DEFAULT_OPTIONS,
    CHEM_DEFAULT_OPTIONS,
    MORPHO_DEFAULT_OPTIONS,
)

def case_list(request, category_slug=None):
    categories = CaseCategory.objects.all()
    selected_category = None
    cases = Case.objects.all()
    if category_slug:
        selected_category = get_object_or_404(CaseCategory, slug=category_slug)
        cases = cases.filter(category=selected_category)
    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'categories': categories,
        'selected_category': selected_category
    })

def case_detail(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    
    # محاسبه ID کیس بعدی و قبلی
    all_cases = Case.objects.order_by('id')
    current_index = list(all_cases.values_list('id', flat=True)).index(case_id)
    
    next_case_id = None
    prev_case_id = None
    
    if current_index < len(all_cases) - 1:
        next_case_id = all_cases[current_index + 1].id
    if current_index > 0:
        prev_case_id = all_cases[current_index - 1].id
    
    # دریافت تست‌های آزمایشگاهی
    lab_tests = case.lab_tests.all()
    
    # دریافت اسلایدها
    slides = case.slides.all()
    
    # دریافت مشاهدات (Test model)
    test_observations = case.tests.all()
    
    # ساخت داده‌های جدول آزمایش به‌صورت گروهی (نمایش حتی بدون Test مرتبط)
    tests_map = {}
    for lt in lab_tests:
        key = lt.test_type.lower()
        # تلاش برای یافتن تست مرتبط با تطبیق انعطاف‌پذیر
        related_test = (
            test_observations.filter(title__iexact=key).first()
            or (test_observations.filter(title__icontains='chem').first() if key in ['chem', 'clinical chemistry'] else None)
            or (test_observations.filter(title__icontains='cbc').first() if key in ['cbc'] else None)
            or (test_observations.filter(title__icontains='slide').first() if key in ['slide'] else None)
        )

        if key not in tests_map:
            tests_map[key] = {
                'title': key,
                'rows': [],
                'observations': (
                    [opt.text for opt in related_test.options.all()] if related_test and hasattr(related_test, 'options') and related_test.options.exists()
                    else (
                        related_test.observations if related_test and related_test.observations else (
                            CBC_DEFAULT_OPTIONS if key == 'cbc' else (
                                CHEM_DEFAULT_OPTIONS if key == 'chem' else (
                                    MORPHO_DEFAULT_OPTIONS if key == 'other' else []
                                )
                            )
                        )
                    )
                ),
                'correct_observations': (
                    [opt.text for opt in related_test.options.filter(is_correct=True)] if related_test and hasattr(related_test, 'options') and related_test.options.exists()
                    else (related_test.correct_observations if related_test and related_test.correct_observations else [])
                ),
            }

        tests_map[key]['rows'].append({
            'name': lt.name,
            'value': lt.value,
            'reference': lt.reference_range,
            'report': lt.report,
        })

    tests_data = list(tests_map.values())

    # اگر هیچ داده‌ای برای CBC/CHEM/OTHER وجود ندارد، ورودی‌های پیش‌فرض اضافه کن
    if not any(t.get('title') == 'cbc' for t in tests_data):
        tests_data.append({
            'title': 'cbc',
            'rows': [],
            'observations': CBC_DEFAULT_OPTIONS,
            'correct_observations': [],
        })
    if not any(t.get('title') == 'chem' for t in tests_data):
        tests_data.append({
            'title': 'chem',
            'rows': [],
            'observations': CHEM_DEFAULT_OPTIONS,
            'correct_observations': [],
        })
    if not any(t.get('title') == 'other' for t in tests_data):
        tests_data.append({
            'title': 'other',
            'rows': [],
            'observations': MORPHO_DEFAULT_OPTIONS,
            'correct_observations': [],
        })
    
    # اضافه کردن اسلایدها به داده‌ها (نمایش حتی بدون Test مرتبط)
    slides_data = []
    for slide in slides:
        slide_test = test_observations.filter(title__iexact='slide').first()

        try:
            if slide.image and slide.image.name:
                report_html = f"<img src='{slide.image.url}' style='max-width:100%; height:auto; border-radius:8px;' /><br><br><strong>توضیحات:</strong> {slide.description}"
            else:
                report_html = f"<div style='background: #f0f0f0; padding: 20px; text-align: center; border-radius:8px;'><i class='fas fa-image' style='font-size: 48px; color: #ccc;'></i><br><br><strong>توضیحات:</strong> {slide.description}</div>"
        except Exception as e:
            print(f"Error processing slide image: {e}")
            report_html = f"<div style='background: #f0f0f0; padding: 20px; text-align: center; border-radius:8px;'><i class='fas fa-image' style='font-size: 48px; color: #ccc;'></i><br><br><strong>توضیحات:</strong> {slide.description}</div>"

        slides_data.append({
            'title': 'slide',
            'report': report_html,
            'observations': (
                [opt.text for opt in slide_test.options.all()] if slide_test and hasattr(slide_test, 'options') and slide_test.options.exists() else (slide_test.observations if slide_test and slide_test.observations else [])
            ),
            'correct_observations': (
                [opt.text for opt in slide_test.options.filter(is_correct=True)] if slide_test and hasattr(slide_test, 'options') and slide_test.options.exists() else (slide_test.correct_observations if slide_test and slide_test.correct_observations else [])
            ),
        })
    
    # ترکیب تست‌ها و اسلایدها
    all_tests = tests_data + slides_data
    
    # اگر هیچ تستی موجود نیست، پیام هشدار نمایش بده
    if not all_tests:
        print("WARNING: No tests found in admin panel for this case!")
        print("Please add tests through the admin panel.")
        print(f"Lab tests count: {lab_tests.count()}")
        print(f"Test observations count: {test_observations.count()}")
        print(f"Slides count: {slides.count()}")
    
    # اگر کاربر لاگین کرده، پیشرفت او را دریافت کن
    user_progress = None
    if request.user.is_authenticated:
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            case=case,
            defaults={'completed': False}
        )
    
    return render(request, 'cases/case_detail.html', {
        'case': case,
        'next_case_id': next_case_id,
        'prev_case_id': prev_case_id,
        'tests': all_tests,
        'user_progress': user_progress,
    })

def debug_case(request, case_id):
    """View برای debug کردن داده‌های کیس"""
    case = get_object_or_404(Case, id=case_id)
    
    context = {
        'case': case,
        'lab_tests': case.lab_tests.all(),
        'slides': case.slides.all(),
        'tests': case.tests.all(),
        'lab_tests_count': case.lab_tests.count(),
        'slides_count': case.slides.count(),
        'tests_count': case.tests.count(),
    }
    
    return render(request, 'cases/debug_case.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'خوش آمدید {user.username}!')
            return redirect('case_list')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    
    return render(request, 'cases/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.')
            return render(request, 'cases/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً استفاده شده است.')
            return render(request, 'cases/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user)
        
        login(request, user)
        messages.success(request, f'حساب کاربری {username} با موفقیت ایجاد شد!')
        return redirect('case_list')
    
    return render(request, 'cases/register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('case_list')

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.update_stats()
    
    # دریافت پیشرفت‌های اخیر
    recent_progress = request.user.case_progress.filter(completed=True).order_by('-completed_at')[:10]
    
    # آمار کلی
    total_cases = Case.objects.count()
    completed_cases = user_profile.total_cases_completed
    remaining_cases = total_cases - completed_cases
    
    context = {
        'user_profile': user_profile,
        'recent_progress': recent_progress,
        'total_cases': total_cases,
        'completed_cases': completed_cases,
        'remaining_cases': remaining_cases,
    }
    
    return render(request, 'cases/profile.html', context)

@login_required
def save_progress(request):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        observation_text = request.POST.get('observation_text')
        is_correct = request.POST.get('is_correct') == 'true'
        
        case = get_object_or_404(Case, id=case_id)
        
        # ذخیره مشاهدات کاربر
        UserObservation.objects.create(
            user=request.user,
            case=case,
            observation_text=observation_text,
            is_correct=is_correct
        )
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})

@login_required
def submit_case_result(request):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        user_diagnosis = request.POST.get('user_diagnosis')
        correct_observations = int(request.POST.get('correct_observations', 0))
        total_observations = int(request.POST.get('total_observations', 0))
        attempts_count = int(request.POST.get('attempts_count', 0))
        
        case = get_object_or_404(Case, id=case_id)
        
        # بررسی صحت تشخیص (ساده - می‌توانید پیچیده‌تر کنید)
        is_diagnosis_correct = user_diagnosis.lower().strip() in case.correct_diagnosis.lower()
        
        # به‌روزرسانی یا ایجاد پیشرفت کاربر
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            case=case,
            defaults={
                'completed': True,
                'correct_observations': correct_observations,
                'total_observations': total_observations,
                'attempts_count': attempts_count,
                'user_diagnosis': user_diagnosis,
                'is_diagnosis_correct': is_diagnosis_correct,
                'completed_at': timezone.now()
            }
        )
        
        if not created:
            user_progress.completed = True
            user_progress.correct_observations = correct_observations
            user_progress.total_observations = total_observations
            user_progress.attempts_count = attempts_count
            user_progress.user_diagnosis = user_diagnosis
            user_progress.is_diagnosis_correct = is_diagnosis_correct
            user_progress.completed_at = timezone.now()
            user_progress.save()
        
        # به‌روزرسانی آمار کاربر
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.update_stats()
        
        return JsonResponse({
            'status': 'success',
            'is_diagnosis_correct': is_diagnosis_correct,
            'accuracy_percentage': user_progress.accuracy_percentage
        })
    
    return JsonResponse({'status': 'error'})

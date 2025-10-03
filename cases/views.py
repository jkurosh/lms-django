from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from dadash_app.decorators import subscription_required_or_admin
from .models import (
    Case,
    LabTest,
    UserProgress,
    UserObservation,
    UserProfile,
    CaseCategory,
    SubCategory,
    CBC_DEFAULT_OPTIONS,
    CHEM_DEFAULT_OPTIONS,
    MORPHO_DEFAULT_OPTIONS,
)

@subscription_required_or_admin
def case_list(request, category_slug=None):
    categories = CaseCategory.objects.all()
    selected_category = None
    cases = Case.objects.filter(is_published=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_id = request.GET.get('category')
    if category_id and category_id != 'all':
        try:
            selected_category = get_object_or_404(CaseCategory, id=category_id)
            cases = cases.filter(category=selected_category)
        except (ValueError, CaseCategory.DoesNotExist):
            pass
    elif category_slug:
        selected_category = get_object_or_404(CaseCategory, slug=category_slug)
        cases = cases.filter(category=selected_category)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        cases = cases.filter(
            Q(title__icontains=search_query) | 
            Q(history__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # مرتب‌سازی
    cases = cases.order_by('-created_at')
    
    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query or '',
    })

@subscription_required_or_admin
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
    
    # دریافت مشاهدات (LabTest model)
    test_observations = case.lab_tests.all()
    
    # ساخت داده‌های جدول آزمایش به‌صورت گروهی (نمایش حتی بدون Test مرتبط)
    tests_map = {}
    for lt in lab_tests:
        key = lt.lab_type.lower()
        # یافتن تست مرتبط با تطبیق دقیق
        related_test = test_observations.filter(lab_type__iexact=lt.lab_type.upper()).first()

        if key not in tests_map:
            tests_map[key] = {
                'title': key,
                'rows': [],
                'observations': (
                    [opt.observation_text for opt in UserObservation.objects.filter(case_test=related_test)] if related_test and key != 'cbc'
                    else (
                        [opt.observation_text for opt in UserObservation.objects.filter(case_test__lab_type='CBC_DEFAULT')] if key == 'cbc'
                        else (
                            [opt.observation_text for opt in UserObservation.objects.filter(case_test__lab_type='CHEM_DEFAULT')] if key == 'chem'
                            else (
                                [opt.observation_text for opt in UserObservation.objects.filter(case_test__lab_type='MORPHO_DEFAULT')] if key == 'morpho'
                                else []
                            )
                        )
                    )
                ),
                'correct_observations': (
                    [opt.observation_text for opt in UserObservation.objects.filter(case_test=related_test, is_correct=True)] if related_test and key != 'cbc'
                    else (
                        [opt.observation_text for opt in UserObservation.objects.filter(case_test__lab_type='CBC_DEFAULT', is_correct=True)] if key == 'cbc'
                        else (
                            [opt.observation_text for opt in UserObservation.objects.filter(case_test__lab_type='CHEM_DEFAULT', is_correct=True)] if key == 'chem'
                            else (
                                [opt.observation_text for opt in UserObservation.objects.filter(case_test__lab_type='MORPHO_DEFAULT', is_correct=True)] if key == 'morpho'
                                else []
                            )
                        )
                    )
                ),
            }

        tests_map[key]['rows'].append({
            'name': lt.lab_name,
            'value': lt.lab_result,
            'reference': lt.normal_range,
            'report': lt.lab_result,
        })

    tests_data = list(tests_map.values())

    # اضافه کردن گزینه‌های پیش‌فرض از دیتابیس
    default_test_types = ['CBC_DEFAULT', 'CHEM_DEFAULT', 'MORPHO_DEFAULT']
    
    for default_type in default_test_types:
        # بررسی آیا این نوع تست در tests_data موجود است
        if not any(t.get('title') == default_type.lower().replace('_default', '') for t in tests_data):
            # پیدا کردن default test در دیتابیس
            default_test = test_observations.filter(lab_type=default_type).first()
            
            if default_test:
                # دریافت observations از دیتابیس
                observations = [opt.observation_text for opt in UserObservation.objects.filter(case_test=default_test)]
                correct_observations = [opt.observation_text for opt in UserObservation.objects.filter(case_test=default_test, is_correct=True)]
                
                test_title = default_type.lower().replace('_default', '')
                tests_data.append({
                    'title': test_title,
                    'rows': [],  # default tests هیچ row ندارند
                    'observations': observations,
                    'correct_observations': correct_observations,
                })
    
    # اضافه کردن اسلایدها به داده‌ها (نمایش حتی بدون Test مرتبط)
    slides_data = []
    for i, slide in enumerate(slides):
        slide_test = test_observations.filter(lab_type__iexact='slide').first()

        try:
            if slide.image and slide.image.strip():
                # slide.image یک CharField است که نام فایل را ذخیره می‌کند
                image_url = f"/media/slides/{slide.image}"
                report_html = f"""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <img src='{image_url}' 
                         style='max-width:100%; height:auto; border-radius:8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);' 
                         alt='{slide.title or "Slide Image"}' 
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />
                    <div style='display:none; background: #f0f0f0; padding: 20px; text-align: center; border-radius:8px;'>
                        <i class='fas fa-image' style='font-size: 48px; color: #ccc;'></i><br>
                        <p>تصویر یافت نشد: {slide.image}</p>
                    </div>
                </div>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-right: 4px solid #3ea66b;">
                    <strong>عنوان:</strong> {slide.title or 'بدون عنوان'}<br><br>
                    <strong>توضیحات:</strong> {slide.description or 'بدون توضیح'}
                </div>
                """
            else:
                report_html = f"""
                <div style='background: #f0f0f0; padding: 20px; text-align: center; border-radius:8px;'>
                    <i class='fas fa-image' style='font-size: 48px; color: #ccc;'></i><br><br>
                    <strong>عنوان:</strong> {slide.title or 'بدون عنوان'}<br><br>
                    <strong>توضیحات:</strong> {slide.description or 'بدون توضیح'}
                </div>
                """
        except Exception as e:
            print(f"Error processing slide image: {e}")
            report_html = f"""
            <div style='background: #f0f0f0; padding: 20px; text-align: center; border-radius:8px;'>
                <i class='fas fa-image' style='font-size: 48px; color: #ccc;'></i><br><br>
                <strong>خطا در نمایش تصویر:</strong> {str(e)}<br><br>
                <strong>عنوان:</strong> {slide.title or 'بدون عنوان'}<br><br>
                <strong>توضیحات:</strong> {slide.description or 'بدون توضیح'}
            </div>
            """

        slides_data.append({
            'title': f'slide_{i+1}',
            'report': report_html,
            'observations': (
                [opt.observation_text for opt in UserObservation.objects.filter(case_test=slide_test)] if slide_test else []
            ),
            'correct_observations': (
                [opt.observation_text for opt in UserObservation.objects.filter(case_test=slide_test, is_correct=True)] if slide_test else []
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
        try:
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                case=case,
                defaults={'completed': False}
            )
        except Exception as e:
            print(f"Error creating user progress: {e}")
            user_progress = None
    
    return render(request, 'cases/case_detail.html', {
        'case': case,
        'next_case_id': next_case_id,
        'prev_case_id': prev_case_id,
        'tests': all_tests,
        'user_progress': user_progress,
        'correct_diagnosis': case.correct_diagnosis or 'تشخیص صحیح در دسترس نیست',
        'diagnosis_explanation': case.explanation or 'توضیحات تکمیلی در دسترس نیست',
    })

def debug_case(request, case_id):
    """View برای debug کردن داده‌های کیس"""
    case = get_object_or_404(Case, id=case_id)
    
    context = {
        'case': case,
        'lab_tests': case.lab_tests.all(),
        'slides': case.slides.all(),
        'tests': case.lab_tests.all(),
        'lab_tests_count': case.lab_tests.count(),
        'slides_count': case.slides.count(),
        'tests_count': case.lab_tests.count(),
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
            return redirect('cases:case_list')
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
        return redirect('cases:case_list')
    
    return render(request, 'cases/register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('cases:case_list')

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
        try:
            case_id = request.POST.get('case_id')
            observation_text = request.POST.get('observation_text')
            is_correct = request.POST.get('is_correct') == 'true'
            
            if not case_id or not observation_text:
                return JsonResponse({'status': 'error', 'error': 'Missing required fields'})
            
            case = get_object_or_404(Case, id=case_id)
            
            # پیدا کردن یا ایجاد یک LabTest پیش‌فرض برای این case
            default_test, created = case.lab_tests.get_or_create(
                lab_type='OBSERVATION',
                defaults={
                    'lab_name': 'User Observation',
                    'lab_result': 'N/A',
                    'normal_range': 'N/A'
                }
            )
            
            # ذخیره مشاهدات کاربر
            UserObservation.objects.create(
                user=request.user,
                case=case,
                case_test=default_test,
                observation_text=observation_text,
                is_correct=is_correct
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'})

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


def get_default_options(request):
    """دریافت گزینه‌های پیش‌فرض برای تست‌های آزمایشگاهی"""
    test_type = request.GET.get('type', 'CBC')
    
    if test_type == 'CBC':
        options = CBC_DEFAULT_OPTIONS
    elif test_type == 'CHEM':
        options = CHEM_DEFAULT_OPTIONS
    elif test_type == 'MORPHO':
        options = MORPHO_DEFAULT_OPTIONS
    else:
        options = []
    
    return JsonResponse({
        'options': options,
        'type': test_type
    })
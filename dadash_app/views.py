from django.shortcuts import render
from django. http import JsonResponse
from cases.models import Case, CaseCategory, LabTest, Slide, Test
from django.db.models import Count

# Create your views here.

def dadash_home(request):
    """صفحه اصلی dadash"""
    categories = CaseCategory.objects.annotate(case_count=Count('cases'))
    
    context = {
        'categories': categories,
        'total_cases': Case.objects.count(),
    }
    return render(request, 'dadash/index.html', context)

def internal_diseases(request):
    """صفحه بیماری‌های داخلی"""
    cases = Case.objects.filter(category__name__icontains='داخلی').prefetch_related('lab_tests', 'slides')
    
    context = {
        'cases': cases,
        'category_name': 'بیماری‌های داخلی',
    }
    return render(request, 'dadash/internal-diseases.html', context)

def surgery(request):
    """صفحه جراحی"""
    cases = Case.objects.filter(category__name__icontains='جراحی').prefetch_related('lab_tests', 'slides')
    
    context = {
        'cases': cases,
        'category_name': 'جراحی',
    }
    return render(request, 'dadash/surgery.html', context)

def emergency(request):
    """صفحه اورژانس"""
    cases = Case.objects.filter(category__name__icontains='اورژانس').prefetch_related('lab_tests', 'slides')
    
    context = {
        'cases': cases,
        'category_name': 'پزشکی اورژانس',
    }
    return render(request, 'dadash/emergency.html', context)

def dermatology(request):
    """صفحه پوست‌شناسی"""
    cases = Case.objects.filter(category__name__icontains='پوست').prefetch_related('lab_tests', 'slides')
    
    context = {
        'cases': cases,
        'category_name': 'پوست‌شناسی',
    }
    return render(request, 'dadash/dermatology.html', context)

def radiology(request):
    """صفحه رادیولوژی"""
    cases = Case.objects.filter(category__name__icontains='رادیولوژی').prefetch_related('lab_tests', 'slides')
    
    context = {
        'cases': cases,
        'category_name': 'رادیولوژی',
    }
    return render(request, 'dadash/radiology.html', context)

def cardiology(request):
    """صفحه قلب‌شناسی"""
    cases = Case.objects.filter(category__name__icontains='قلب').prefetch_related('lab_tests', 'slides')
    
    context = {
        'cases': cases,
        'category_name': 'قلب‌شناسی',
    }
    return render(request, 'dadash/cardiology.html', context)

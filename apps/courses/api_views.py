from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Case, CaseCategory, LabTest, UserProgress, UserObservation
from .serializers import (
    CaseSerializer, CaseListSerializer, CaseCategorySerializer,
    LabTestSerializer, UserProgressSerializer, UserObservationSerializer
)

class CaseListView(generics.ListAPIView):
    """
    لیست تمام مطالعات موردی با قابلیت فیلتر و جستجو
    """
    queryset = Case.objects.all().prefetch_related('category', 'lab_tests', 'slides')
    serializer_class = CaseListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty_level']
    search_fields = ['title', 'history', 'category__name']
    ordering_fields = ['created_at', 'title', 'difficulty_level']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category_slug', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

class CaseDetailView(generics.RetrieveAPIView):
    """
    جزئیات یک مطالعه موردی
    """
    queryset = Case.objects.all().prefetch_related('category', 'subcategory', 'lab_tests', 'slides')
    serializer_class = CaseSerializer

class CategoryListView(generics.ListAPIView):
    """
    لیست تمام دسته‌بندی‌ها
    """
    queryset = CaseCategory.objects.all()
    serializer_class = CaseCategorySerializer

class LabTestListView(generics.ListAPIView):
    """
    لیست آزمایش‌های یک مطالعه موردی
    """
    serializer_class = LabTestSerializer
    
    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return LabTest.objects.filter(case_id=case_id)

@api_view(['GET'])
def case_stats(request):
    """
    آمار کلی مطالعات موردی
    """
    total_cases = Case.objects.count()
    categories = CaseCategory.objects.all()
    category_stats = []
    
    for category in categories:
        case_count = Case.objects.filter(category=category).count()
        category_stats.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'count': case_count
        })
    
    return Response({
        'total_cases': total_cases,
        'categories': category_stats
    })

@api_view(['POST'])
def create_user_progress(request):
    """
    ایجاد یا به‌روزرسانی پیشرفت کاربر
    """
    serializer = UserProgressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user_observation(request):
    """
    ایجاد مشاهده کاربر
    """
    serializer = UserObservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_progress_list(request, user_id):
    """
    لیست پیشرفت‌های کاربر
    """
    progress = UserProgress.objects.filter(user_id=user_id)
    serializer = UserProgressSerializer(progress, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_cases(request):
    """
    جستجوی پیشرفته در مطالعات موردی
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    
    queryset = Case.objects.all()
    
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | 
            Q(history__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    if category:
        queryset = queryset.filter(category__slug=category)
    
    if difficulty:
        queryset = queryset.filter(difficulty_level=difficulty)
    
    serializer = CaseListSerializer(queryset, many=True)
    return Response(serializer.data)

from rest_framework import serializers
from .models import Case, CaseCategory, LabTest, UserProgress, UserObservation, UserProfile, SubCategory

class CaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseCategory
        fields = ['id', 'name', 'slug', 'description']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'description']

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['id', 'name', 'test_type', 'normal_range', 'unit', 'description']

class CaseSerializer(serializers.ModelSerializer):
    category = CaseCategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    lab_tests = LabTestSerializer(many=True, read_only=True)
    slides_count = serializers.SerializerMethodField()
    lab_tests_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        fields = [
            'id', 'title', 'history', 'physical_examination', 
            'category', 'subcategory', 'difficulty_level',
            'estimated_time', 'created_at', 'updated_at',
            'lab_tests', 'slides_count', 'lab_tests_count'
        ]
    
    def get_slides_count(self, obj):
        return obj.slides.count()
    
    def get_lab_tests_count(self, obj):
        return obj.lab_tests.count()

class CaseListSerializer(serializers.ModelSerializer):
    category = CaseCategorySerializer(read_only=True)
    slides_count = serializers.SerializerMethodField()
    lab_tests_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        fields = [
            'id', 'title', 'history', 'category', 'difficulty_level',
            'estimated_time', 'created_at', 'slides_count', 'lab_tests_count'
        ]
    
    def get_slides_count(self, obj):
        return obj.slides.count()
    
    def get_lab_tests_count(self, obj):
        return obj.lab_tests.count()

class UserProgressSerializer(serializers.ModelSerializer):
    case_title = serializers.CharField(source='case.title', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'case', 'case_title', 'current_step', 'is_completed',
            'score', 'started_at', 'completed_at', 'final_diagnosis'
        ]

class UserObservationSerializer(serializers.ModelSerializer):
    case_title = serializers.CharField(source='case.title', read_only=True)
    
    class Meta:
        model = UserObservation
        fields = [
            'id', 'case', 'case_title', 'observation_type', 'observation_value',
            'is_correct', 'created_at'
        ]

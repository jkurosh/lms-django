from django.core.management.base import BaseCommand
from apps.courses.models import Case, LabTest, Test, CaseCategory


class Command(BaseCommand):
    help = 'Debug کردن داده‌های موجود در دیتابیس'

    def handle(self, *args, **options):
        self.stdout.write("=== DEBUG DATA ===")
        
        # بررسی کیس‌ها
        cases = Case.objects.all()
        self.stdout.write(f"\nتعداد کل کیس‌ها: {cases.count()}")
        
        for case in cases:
            self.stdout.write(f"\n--- کیس ID: {case.id} ---")
            self.stdout.write(f"عنوان: {case.title}")
            self.stdout.write(f"دسته‌بندی: {case.category.name if case.category else 'بدون دسته'}")
            
            # بررسی تست‌های آزمایشگاهی
            lab_tests = case.lab_tests.all()
            self.stdout.write(f"تست‌های آزمایشگاهی: {lab_tests.count()}")
            for lt in lab_tests:
                self.stdout.write(f"  - {lt.test_type}: {lt.name} = {lt.value}")
            
            # بررسی مشاهدات
            tests = case.tests.all()
            self.stdout.write(f"مشاهدات: {tests.count()}")
            for t in tests:
                self.stdout.write(f"  - {t.title}: {len(t.observations)} مشاهده")
                self.stdout.write(f"    مشاهدات: {t.observations}")
                self.stdout.write(f"    پاسخ‌های صحیح: {t.correct_observations}")
            
            # بررسی اسلایدها
            slides = case.slides.all()
            self.stdout.write(f"اسلایدها: {slides.count()}")
        
        # بررسی دسته‌بندی‌ها
        categories = CaseCategory.objects.all()
        self.stdout.write(f"\n=== دسته‌بندی‌ها ===")
        for cat in categories:
            self.stdout.write(f"- {cat.name} ({cat.slug}): {cat.cases.count()} کیس")
        
        self.stdout.write("\n=== END DEBUG ===") 
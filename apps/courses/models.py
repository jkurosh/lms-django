from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# گزینه‌های پیش‌فرض برای تست CBC
CBC_DEFAULT_OPTIONS = [
    'Polycythemia',
    'No abnormalities',
    'Mild nonregenerative anemia',
    'Mild regenerative anemia',
    'Neutrophilia',
    'Neutropenia',
    'Lymphopenia',
    'Lymphocytosis',
    'Eosinophilia',
    'Eosinopenia',
    'Monocytosis',
]

# گزینه‌های پیش‌فرض برای شیمی بالینی (CHEM)
CHEM_DEFAULT_OPTIONS = [
    'No abnormalities',
    'Physiological hypoglycemia',
    'Physiological hyperglycemia',
    'Significative hyperglycemia',
    'Artifactual hypoglycemia',
    'Uremia',
    'Low urea',
    'High liver enzymes',
    'Hyperproteinemia',
    'Hypoproteinemia',
    'Hypoalbuminemia',
    'Hyperglobulinemia',
    'Physiological hypercalcemia',
    'Significant hypercalcemia',
    'Hypocalcemia (hypoalbuminemia)',
    'Significant hypocalcemia',
    'Hyperphosphatemia',
    'Hyperkalemia',
    'Hypokalemia',
    'Hypernatremia',
    'Hyponatremia',
    'Hyperchloremia',
    'Hypochloremia',
    'High anion gap metabolic acidosis',
    'Hyperchloremic metabolic acidosis',
    'Metabolic alkalosis',
    'Mixed acid-base disorder',
]

# گزینه‌های پیش‌فرض تغییرات مورفولوژیک (MORPHO)
MORPHO_DEFAULT_OPTIONS = [
    'No abnormalities',
    'Reactive lymphocytes',
    'Circulating blasts',
    'Spherocytes',
    'Acanthocytes',
    'Keratocytes',
    'Schizocytes',
    'Heinz bodies',
    'Howell-Joly bodies',
    'Autoagglutination',
    'Microcytosis',
    'Megaloblasts',
    'Nucleated red blood cells',
    'Toxic neutrophils',
    'Immature neutrophils',
]

TEST_TYPES = [
    ('CBC', 'CBC'),
    ('CHEM', 'Clinical Chemistry'),
    ('OTHER', 'Other Tests'),
    ('SLIDE', 'Slides')
]

# گزینه‌های پیش‌فرض برای تست CBC
CBC_DEFAULT_OPTIONS = [
    'Polycythemia',
    'No abnormalities',
    'Mild nonregenerative anemia',
    'Mild regenerative anemia',
    'Neutrophilia',
    'Neutropenia',
    'Lymphopenia',
    'Lymphocytosis',
    'Eosinophilia',
    'Eosinopenia',
    'Monocytosis',
]

# گزینه‌های پیش‌فرض تغییرات مورفولوژیک (CBC)
MORPHO_DEFAULT_OPTIONS = [
    'No abnormalities',
    'Reactive lymphocytes',
    'Circulating blasts',
    'Spherocytes',
    'Acanthocytes',
    'Keratocytes',
    'Schizocytes',
    'Heinz bodies',
    'Howell-Joly bodies',
    'Autoagglutination',
    'Microcytosis',
    'Megaloblasts',
    'Nucleated red blood cells',
    'Toxic neutrophils',
    'Immature neutrophils',
]

# گزینه‌های پیش‌فرض برای شیمی بالینی (CHEM)
CHEM_DEFAULT_OPTIONS = [
    'No abnormalities',
    'Physiological hypoglycemia',
    'Physiological hyperglycemia',
    'Significative hyperglycemia',
    'Artifactual hypoglycemia',
    'Uremia',
    'Low urea',
    'High liver enzymes',
    'Hyperproteinemia',
    'Hypoproteinemia',
    'Hypoalbuminemia',
    'Hyperglobulinemia',
    'Physiological hypercalcemia',
    'Significant hypercalcemia',
    'Hypocalcemia (hypoalbuminemia)',
    'Significant hypocalcemia',
    'Hyperphosphatemia',
    'Hyperkalemia',
    'Hypokalemia',
    'Hypernatremia',
    'Hyponatremia',
    'Hyperchloremia',
    'Hypochloremia',
    'High anion gap metabolic acidosis',
    'Hyperchloremic metabolic acidosis',
    'Metabolic alkalosis',
    'Mixed acid-base disorder',
]

class CaseCategory(models.Model):
    name = models.TextField(unique=True)
    slug = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "دسته‌بندی کیس"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']
        db_table = 'courses_casecategory'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(CaseCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.TextField()
    slug = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "زیردسته‌بندی"
        verbose_name_plural = "زیردسته‌بندی‌ها"
        ordering = ['name']
        db_table = 'courses_subcategory'

    def __str__(self):
        return self.name

class Case(models.Model):
    category = models.ForeignKey(CaseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    title = models.TextField()
    slug = models.TextField(unique=True, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    history = models.TextField(blank=True, null=True, verbose_name="پیشینه")
    correct_diagnosis = models.TextField(blank=True, null=True, verbose_name="تشخیص صحیح")
    explanation = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        db_table = 'courses_case'

class LabTest(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='lab_tests', db_column='case_study_id')
    lab_name = models.TextField(blank=True, null=True)
    normal_range = models.TextField(blank=True, null=True)
    lab_result = models.TextField(blank=True, null=True)
    lab_type = models.CharField(max_length=50)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'case_tests'

    def __str__(self):
        return f"{self.lab_name} ({self.lab_type})"

class Slide(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='slides', db_column='case_id')
    image = models.CharField(max_length=100)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses_slide'

    def __str__(self):
        return f"Slide for {self.case.title}"

# Test model حذف شد چون با LabTest تداخل داشت

# TestOption model حذف شد چون به Test وابسته بود

# Signal حذف شد چون Test model حذف شد

# مدل‌های جدید برای پیگیری عملکرد کاربران - بر اساس اسکیما دیتابیس
class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='case_progress', db_column='user_id')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='user_progress', db_column='case_study_id')
    completed = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    attempts = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_test = models.ForeignKey(LabTest, on_delete=models.SET_NULL, null=True, blank=True, db_column='last_test_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_progress'

    def __str__(self):
        return f"{self.user.username} - {self.case.title}"

    @property
    def accuracy_percentage(self):
        if self.score is None:
            return 0
        return float(self.score)

class Test(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=100, choices=[
        ('cbc', 'CBC'),
        ('chem', 'Clinical Chemistry'),
        ('morpho', 'Morphological Changes'),
        ('other', 'Other Tests'),
        ('slide', 'Slides')
    ])
    report = models.TextField(blank=True, null=True)
    observations = models.JSONField(default=list, blank=True)
    correct_observations = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tests'
        unique_together = ('case', 'title')

    def __str__(self):
        return f"{self.case.title} - {self.get_title_display()}"

# TestOption model حذف شد چون با UserObservation تداخل داشت

class UserObservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_observations')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='user_observations', null=True, blank=True)
    case_test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='options', db_column='case_test_id', null=True, blank=True)
    observation_text = models.TextField(db_column='option_text', null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(null=True, blank=True)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'case_options'

    def __str__(self):
        return f"{self.observation_text or 'Unknown'} - {self.is_correct or False}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    total_cases_completed = models.IntegerField(default=0)
    total_correct_observations = models.IntegerField(default=0)
    total_observations = models.IntegerField(default=0)
    total_correct_diagnoses = models.IntegerField(default=0)
    total_diagnoses = models.IntegerField(default=0)
    average_attempts_per_case = models.FloatField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses_userprofile'

    def __str__(self):
        return f"Profile for {self.user.username}"

    @property
    def overall_accuracy(self):
        if self.total_observations == 0:
            return 0
        return round((self.total_correct_observations / self.total_observations) * 100, 1)

    @property
    def diagnosis_accuracy(self):
        if self.total_diagnoses == 0:
            return 0
        return round((self.total_correct_diagnoses / self.total_diagnoses) * 100, 1)

    @property
    def is_subscription_active(self):
        if not self.subscription_start or not self.subscription_end:
            return False
        now = timezone.now()
        return self.subscription_start <= now <= self.subscription_end

    def set_subscription(self, start_dt, end_dt):
        self.subscription_start = start_dt
        self.subscription_end = end_dt
        self.save(update_fields=['subscription_start', 'subscription_end'])

    def update_stats(self):
        """به‌روزرسانی آمار کاربر"""
        progress_records = self.user.case_progress.filter(completed=True)
        
        self.total_cases_completed = progress_records.count()
        self.total_correct_observations = sum(p.correct_observations for p in progress_records)
        self.total_observations = sum(p.total_observations for p in progress_records)
        self.total_correct_diagnoses = progress_records.filter(is_diagnosis_correct=True).count()
        self.total_diagnoses = progress_records.count()
        
        if self.total_cases_completed > 0:
            self.average_attempts_per_case = sum(p.attempts_count for p in progress_records) / self.total_cases_completed
        
        self.save()


class Bookmark(models.Model):
    """مدل برای bookmark کردن case ها"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="یادداشت‌های شخصی برای این case")
    
    class Meta:
        unique_together = ('user', 'case')
        ordering = ['-created_at']
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        db_table = 'courses_bookmark'
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.case.title}"


@receiver(post_save, sender=Case)
def create_default_lab_tests_for_case(sender, instance, created, **kwargs):
    """ایجاد تست‌های پیش‌فرض برای کیس جدید"""
    if created:
        # ایجاد تست CBC
        cbc_test = LabTest.objects.create(
            case=instance,
            lab_type='CBC',
            lab_name='Complete Blood Count',
            normal_range='Normal ranges vary by species',
            lab_result='',
            order_index=1
        )
        
        # ایجاد تست CHEM
        chem_test = LabTest.objects.create(
            case=instance,
            lab_type='CHEM',
            lab_name='Clinical Chemistry Panel',
            normal_range='Normal ranges vary by species',
            lab_result='',
            order_index=2
        )
        
        # ایجاد تست MORPHO
        morpho_test = LabTest.objects.create(
            case=instance,
            lab_type='MORPHO',
            lab_name='Morphological Changes',
            normal_range='No abnormalities expected',
            lab_result='',
            order_index=3
        )
        
        # ایجاد گزینه‌های پیش‌فرض برای UserObservation
        create_default_user_observations(instance, cbc_test, chem_test, morpho_test)


def create_default_user_observations(case, cbc_test, chem_test, morpho_test):
    """ایجاد گزینه‌های پیش‌فرض UserObservation برای تست‌های مختلف"""
    
    # ایجاد UserObservation برای CBC
    for i, option in enumerate(CBC_DEFAULT_OPTIONS):
        UserObservation.objects.create(
            case=case,
            case_test=cbc_test,
            observation_text=option,
            is_correct=False,  # به صورت پیش‌فرض غلط
            explanation="",
            order_index=i
        )
    
    # ایجاد UserObservation برای CHEM
    for i, option in enumerate(CHEM_DEFAULT_OPTIONS):
        UserObservation.objects.create(
            case=case,
            case_test=chem_test,
            observation_text=option,
            is_correct=False,  # به صورت پیش‌فرض غلط
            explanation="",
            order_index=i
        )
    
    # ایجاد UserObservation برای MORPHO
    for i, option in enumerate(MORPHO_DEFAULT_OPTIONS):
        UserObservation.objects.create(
            case=case,
            case_test=morpho_test,
            observation_text=option,
            is_correct=False,  # به صورت پیش‌فرض غلط
            explanation="",
            order_index=i
        )
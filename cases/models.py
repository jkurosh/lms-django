from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True, help_text="اختیاری؛ ایموجی یا آیکن کوتاه")

    class Meta:
        verbose_name = "دسته‌بندی کیس"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

class Case(models.Model):
    category = models.ForeignKey(CaseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    title = models.CharField(max_length=200)
    history = models.TextField()
    correct_diagnosis = models.TextField()
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

class LabTest(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='lab_tests')
    test_type = models.CharField(max_length=10, choices=TEST_TYPES)
    name = models.CharField(max_length=100)  # مثل Hematocrit
    reference_range = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    report = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.test_type})"

class Slide(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='slides/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Slide for {self.case.title}"

class Test(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=100)  # مثلاً CBC, CLIN.CHEMISTRY
    report = models.TextField()
    observations = models.JSONField(blank=True, null=True)  # برای سازگاری قدیمی
    correct_observations = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} for {self.case.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # اگر تست CBC / CHEM / OTHER است و تازه ایجاد شده و هنوز گزینه‌ای ندارد، گزینه‌های پیش‌فرض را بساز
        title_normalized = (self.title or '').strip().lower()
        if is_new and title_normalized in ('cbc', 'chem', 'other') and not self.options.exists():
            if title_normalized == 'cbc':
                defaults = CBC_DEFAULT_OPTIONS
            elif title_normalized == 'chem':
                defaults = CHEM_DEFAULT_OPTIONS
            else:
                defaults = MORPHO_DEFAULT_OPTIONS
            if not self.observations:
                self.observations = defaults
            if not self.correct_observations:
                self.correct_observations = []
            super().save(update_fields=['observations', 'correct_observations'])

            for idx, text in enumerate(defaults):
                TestOption.objects.create(test=self, text=text, is_correct=False, order_index=idx)

class TestOption(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order_index', 'id']

    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"

# ایجاد خودکار تست‌های پیش‌فرض برای هر کیس جدید
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Case)
def create_default_tests_for_case(sender, instance: Case, created: bool, **kwargs):
    if not created:
        return
    # اگر تستی موجود نیست، تست‌های پیش‌فرض بساز
    if instance.tests.exists():
        return
    defaults_map = {
        'cbc': CBC_DEFAULT_OPTIONS,
        'chem': CHEM_DEFAULT_OPTIONS,
        'other': MORPHO_DEFAULT_OPTIONS,
    }
    for title, options in defaults_map.items():
        test = Test.objects.create(case=instance, title=title, report='')
        # پر کردن JSON برای سازگاری
        test.observations = options
        test.correct_observations = []
        test.save(update_fields=['observations', 'correct_observations'])
        # ایجاد TestOption ها
        for idx, text in enumerate(options):
            TestOption.objects.create(test=test, text=text, is_correct=False, order_index=idx)

# مدل‌های جدید برای پیگیری عملکرد کاربران
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_progress')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    correct_observations = models.IntegerField(default=0)
    total_observations = models.IntegerField(default=0)
    attempts_count = models.IntegerField(default=0)
    user_diagnosis = models.TextField(blank=True)
    is_diagnosis_correct = models.BooleanField(null=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'case']
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.case.title}"

    @property
    def accuracy_percentage(self):
        if self.total_observations == 0:
            return 0
        return round((self.correct_observations / self.total_observations) * 100, 1)

class UserObservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observations')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='user_observations')
    observation_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.observation_text}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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

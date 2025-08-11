from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

TEST_TYPES = [
    ('CBC', 'CBC'),
    ('CHEM', 'Clinical Chemistry'),
    ('OTHER', 'Other Tests'),
    ('SLIDE', 'Slides')
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
    observations = models.JSONField()  # یه لیست از گزینه‌ها
    correct_observations = models.JSONField()

    def __str__(self):
        return f"{self.title} for {self.case.title}"

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

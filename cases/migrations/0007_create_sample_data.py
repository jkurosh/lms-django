# Generated manually to create sample data

from django.db import migrations


def create_sample_data(apps, schema_editor):
    CaseCategory = apps.get_model('cases', 'CaseCategory')
    SubCategory = apps.get_model('cases', 'SubCategory')
    
    # ایجاد دسته‌بندی‌های اصلی
    categories_data = [
        {'name': 'بیماری‌های داخلی', 'slug': 'internal-diseases'},
        {'name': 'جراحی', 'slug': 'surgery'},
        {'name': 'زنان و زایمان', 'slug': 'gynecology'},
        {'name': 'اطفال', 'slug': 'pediatrics'},
        {'name': 'روانپزشکی', 'slug': 'psychiatry'},
    ]
    
    for cat_data in categories_data:
        CaseCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name']}
        )
    
    # ایجاد زیردسته‌بندی‌ها
    subcategories_data = [
        {'name': 'بیماری‌های قلبی', 'category_slug': 'internal-diseases'},
        {'name': 'بیماری‌های گوارشی', 'category_slug': 'internal-diseases'},
        {'name': 'بیماری‌های تنفسی', 'category_slug': 'internal-diseases'},
        {'name': 'جراحی عمومی', 'category_slug': 'surgery'},
        {'name': 'جراحی قلب', 'category_slug': 'surgery'},
        {'name': 'جراحی مغز و اعصاب', 'category_slug': 'surgery'},
        {'name': 'زایمان طبیعی', 'category_slug': 'gynecology'},
        {'name': 'سزارین', 'category_slug': 'gynecology'},
        {'name': 'بیماری‌های نوزادان', 'category_slug': 'pediatrics'},
        {'name': 'بیماری‌های کودکان', 'category_slug': 'pediatrics'},
    ]
    
    for sub_data in subcategories_data:
        try:
            category = CaseCategory.objects.get(slug=sub_data['category_slug'])
            SubCategory.objects.get_or_create(
                name=sub_data['name'],
                category=category,
                defaults={'slug': sub_data['name'].lower().replace(' ', '-')}
            )
        except CaseCategory.DoesNotExist:
            pass


def reverse_create_sample_data(apps, schema_editor):
    # حذف داده‌های نمونه (اختیاری)
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0006_remove_unnecessary_fields'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, reverse_create_sample_data),
    ]

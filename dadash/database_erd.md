# Veterinary Case Study Database - Entity Relationship Diagram

## Database Schema Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    category     │    │   sub_category   │    │   case_study    │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)          │    │ id (PK)         │
│ name            │◄───┤ category_id (FK) │◄───┤ sub_category_id │
│ description     │    │ name             │    │ title           │
│ is_active       │    │ description      │    │ patient_history │
│ sort_order      │    │ is_active        │    │ difficulty_level│
│ created_at      │    │ sort_order       │    │ estimated_time  │
│ updated_at      │    │ created_at       │    │ is_active       │
└─────────────────┘    │ updated_at       │    │ created_at      │
                       └──────────────────┘    │ updated_at      │
                                                └─────────────────┘
                                                         │
                                                         │
                    ┌────────────────────────────────────┼────────────────────────────────────┐
                    │                                    │                                    │
                    ▼                                    ▼                                    ▼
            ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
            │   case_test     │              │  case_option    │              │case_explanation │
            ├─────────────────┤              ├─────────────────┤              ├─────────────────┤
            │ id (PK)         │              │ id (PK)         │              │ id (PK)         │
            │ case_study_id   │              │ case_study_id   │              │ case_study_id   │
            │ test_name       │              │ option_text     │              │ explanation_text│
            │ test_description│              │ is_correct      │              │ key_learning_pts│
            │ test_result     │              │ sort_order      │              │ references      │
            │ image_url       │              │ explanation_hint│              │ created_at      │
            │ image_alt_text  │              │ created_at      │              │ updated_at      │
            │ sort_order      │              │ updated_at      │              └─────────────────┘
            │ is_required     │              └─────────────────┘
            │ created_at      │
            │ updated_at      │
            └─────────────────┘

┌─────────────────┐    ┌──────────────────┐
│      user       │    │  user_progress   │
├─────────────────┤    ├──────────────────┤
│ id (PK)         │    │ id (PK)          │
│ username        │    │ user_id (FK)     │
│ email           │◄───┤ case_study_id    │
│ password_hash   │    │ selected_option  │
│ first_name      │    │ is_correct       │
│ last_name       │    │ time_spent_sec   │
│ role            │    │ completed_at     │
│ is_active       │    │ created_at       │
│ last_login      │    │ updated_at       │
│ created_at      │    └──────────────────┘
│ updated_at      │
└─────────────────┘
```

## Table Relationships

### Primary Relationships
1. **category** → **sub_category** (1:N)
   - One category can have many subcategories
   - Foreign key: `sub_category.category_id` → `category.id`

2. **sub_category** → **case_study** (1:N)
   - One subcategory can have many cases
   - Foreign key: `case_study.sub_category_id` → `sub_category.id`

3. **case_study** → **case_test** (1:N)
   - One case can have many diagnostic tests
   - Foreign key: `case_test.case_study_id` → `case_study.id`

4. **case_study** → **case_option** (1:N)
   - One case can have many answer options
   - Foreign key: `case_option.case_study_id` → `case_study.id`

5. **case_study** → **case_explanation** (1:1)
   - One case has exactly one explanation
   - Foreign key: `case_explanation.case_study_id` → `case_study.id`

### User Management Relationships
6. **user** → **user_progress** (1:N)
   - One user can have progress records for many cases
   - Foreign key: `user_progress.user_id` → `user.id`

7. **case_study** → **user_progress** (1:N)
   - One case can have progress records from many users
   - Foreign key: `user_progress.case_study_id` → `case_study.id`

8. **case_option** → **user_progress** (1:N)
   - One option can be selected by many users
   - Foreign key: `user_progress.selected_option_id` → `case_option.id`

## Key Features

### Normalization (3NF)
- ✅ **1NF**: All attributes are atomic
- ✅ **2NF**: No partial dependencies
- ✅ **3NF**: No transitive dependencies

### Performance Optimizations
- **Indexes** on all foreign keys
- **Composite indexes** for common query patterns
- **Views** for complex queries
- **Stored procedures** for common operations

### Scalability Features
- **Soft deletes** using `is_active` flags
- **Timestamp tracking** for audit trails
- **Sort order** fields for flexible ordering
- **Extensible user system** for future features

### Data Integrity
- **Foreign key constraints** with appropriate actions
- **Unique constraints** where needed
- **Check constraints** for data validation
- **Default values** for common fields

## Sample Data Flow

```
1. User selects a category (Internal Diseases)
2. System shows subcategories (Gastrointestinal, Cardiovascular, etc.)
3. User selects a subcategory (Gastrointestinal)
4. System displays available cases
5. User selects a case and sees:
   - Patient history
   - Diagnostic tests (with optional images)
   - Multiple choice options
6. User selects an answer
7. System shows explanation and tracks progress
```

## Future Extensions

The schema is designed to support:
- **User authentication and authorization**
- **Progress tracking and analytics**
- **Case ratings and reviews**
- **Discussion forums**
- **Mobile app integration**
- **API endpoints**
- **Multi-language support** 
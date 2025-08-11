# راهنمای مقیاس‌پذیری و بهینه‌سازی پایگاه داده دامپزشکی

## 📊 استراتژی‌های مقیاس‌پذیری

### 1. مقیاس‌پذیری عمودی (Vertical Scaling)

#### بهینه‌سازی سرور
```sql
-- تنظیمات MySQL برای عملکرد بهتر
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB
SET GLOBAL innodb_log_file_size = 268435456; -- 256MB
SET GLOBAL innodb_flush_log_at_trx_commit = 2;
SET GLOBAL innodb_flush_method = 'O_DIRECT';
```

#### بهینه‌سازی کوئری‌ها
```sql
-- استفاده از EXPLAIN برای تحلیل کوئری‌ها
EXPLAIN SELECT 
    c.title,
    sc.name AS subcategory,
    cat.name AS category
FROM case_study c
JOIN sub_category sc ON c.sub_category_id = sc.id
JOIN category cat ON sc.category_id = cat.id
WHERE c.is_active = TRUE;

-- بهینه‌سازی کوئری‌های پیچیده
SELECT 
    c.id,
    c.title,
    COUNT(ct.id) AS test_count,
    COUNT(co.id) AS option_count
FROM case_study c
LEFT JOIN case_test ct ON c.id = ct.case_study_id
LEFT JOIN case_option co ON c.id = co.case_study_id
WHERE c.is_active = TRUE
GROUP BY c.id, c.title
HAVING test_count > 0 AND option_count > 0;
```

### 2. مقیاس‌پذیری افقی (Horizontal Scaling)

#### Sharding Strategy
```sql
-- Sharding بر اساس دسته‌بندی
-- Database 1: Internal Diseases, Surgery
-- Database 2: Emergency Medicine, Dermatology
-- Database 3: Radiology, Other

-- مثال برای Sharding
CREATE TABLE case_study_shard_1 LIKE case_study;
CREATE TABLE case_study_shard_2 LIKE case_study;
CREATE TABLE case_study_shard_3 LIKE case_study;

-- Partitioning بر اساس تاریخ
ALTER TABLE case_study 
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

#### Read Replicas
```sql
-- تنظیمات Master-Slave
-- Master: برای عملیات نوشتن
-- Slave 1: برای کوئری‌های خواندن
-- Slave 2: برای گزارش‌گیری

-- مثال کوئری بر اساس نوع عملیات
-- Master
INSERT INTO case_study (sub_category_id, title, patient_history) 
VALUES (1, 'New Case', 'Patient history...');

-- Slave
SELECT * FROM case_study WHERE is_active = TRUE;
```

### 3. Caching Strategy

#### Redis Caching
```php
// مثال PHP با Redis
class CaseStudyCache {
    private $redis;
    
    public function getCase($caseId) {
        $cacheKey = "case:{$caseId}";
        $cached = $this->redis->get($cacheKey);
        
        if ($cached) {
            return json_decode($cached, true);
        }
        
        // از پایگاه داده بخوان
        $case = $this->getCaseFromDB($caseId);
        
        // در کش ذخیره کن (1 ساعت)
        $this->redis->setex($cacheKey, 3600, json_encode($case));
        
        return $case;
    }
    
    public function invalidateCase($caseId) {
        $this->redis->del("case:{$caseId}");
    }
}
```

#### Application-Level Caching
```sql
-- جداول کش برای داده‌های پرتکرار
CREATE TABLE cache_category_stats (
    category_id INT PRIMARY KEY,
    case_count INT,
    avg_difficulty DECIMAL(3,2),
    last_updated TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- به‌روزرسانی خودکار آمار
CREATE EVENT update_category_stats
ON SCHEDULE EVERY 1 HOUR
DO
    INSERT INTO cache_category_stats (category_id, case_count, avg_difficulty, last_updated)
    SELECT 
        cat.id,
        COUNT(c.id),
        AVG(CASE 
            WHEN c.difficulty_level = 'beginner' THEN 1
            WHEN c.difficulty_level = 'intermediate' THEN 2
            WHEN c.difficulty_level = 'advanced' THEN 3
        END),
        NOW()
    FROM category cat
    LEFT JOIN sub_category sc ON cat.id = sc.category_id
    LEFT JOIN case_study c ON sc.id = c.sub_category_id AND c.is_active = TRUE
    WHERE cat.is_active = TRUE
    GROUP BY cat.id
    ON DUPLICATE KEY UPDATE
        case_count = VALUES(case_count),
        avg_difficulty = VALUES(avg_difficulty),
        last_updated = NOW();
```

## 🔧 بهینه‌سازی عملکرد

### 1. ایندکس‌های پیشرفته

#### ایندکس‌های ترکیبی
```sql
-- ایندکس‌های ترکیبی برای کوئری‌های رایج
CREATE INDEX idx_case_study_subcategory_active_difficulty 
ON case_study(sub_category_id, is_active, difficulty_level);

CREATE INDEX idx_case_test_case_sort_required 
ON case_test(case_study_id, sort_order, is_required);

CREATE INDEX idx_user_progress_user_case_date 
ON user_progress(user_id, case_study_id, completed_at);

-- ایندکس‌های فیلتر شده
CREATE INDEX idx_case_study_active_title 
ON case_study(title) WHERE is_active = TRUE;

CREATE INDEX idx_case_option_correct_case 
ON case_option(case_study_id, is_correct) WHERE is_correct = TRUE;
```

#### ایندکس‌های Full-Text
```sql
-- جستجوی متنی در عنوان و تاریخچه
CREATE FULLTEXT INDEX idx_case_study_search 
ON case_study(title, patient_history);

-- جستجوی پیشرفته
SELECT 
    c.id,
    c.title,
    MATCH(c.title, c.patient_history) AGAINST('pancreatitis vomiting' IN BOOLEAN MODE) AS relevance
FROM case_study c
WHERE MATCH(c.title, c.patient_history) AGAINST('pancreatitis vomiting' IN BOOLEAN MODE)
ORDER BY relevance DESC;
```

### 2. بهینه‌سازی جداول

#### Compression
```sql
-- فشرده‌سازی جداول بزرگ
ALTER TABLE case_study ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
ALTER TABLE case_test ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
ALTER TABLE user_progress ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
```

#### Archiving Strategy
```sql
-- جدول آرشیو برای داده‌های قدیمی
CREATE TABLE case_study_archive LIKE case_study;

-- انتقال داده‌های قدیمی
INSERT INTO case_study_archive 
SELECT * FROM case_study 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR)
AND is_active = FALSE;

DELETE FROM case_study 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR)
AND is_active = FALSE;
```

### 3. بهینه‌سازی کوئری‌ها

#### Stored Procedures بهینه
```sql
DELIMITER //

CREATE PROCEDURE GetCasesByFilters(
    IN p_category_id INT,
    IN p_difficulty_level VARCHAR(20),
    IN p_limit INT,
    IN p_offset INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    SELECT 
        c.id,
        c.title,
        c.difficulty_level,
        c.estimated_time_minutes,
        sc.name AS subcategory_name,
        cat.name AS category_name,
        COUNT(ct.id) AS test_count,
        COUNT(co.id) AS option_count
    FROM case_study c
    JOIN sub_category sc ON c.sub_category_id = sc.id
    JOIN category cat ON sc.category_id = cat.id
    LEFT JOIN case_test ct ON c.id = ct.case_study_id
    LEFT JOIN case_option co ON c.id = co.case_study_id
    WHERE c.is_active = TRUE
    AND (p_category_id IS NULL OR cat.id = p_category_id)
    AND (p_difficulty_level IS NULL OR c.difficulty_level = p_difficulty_level)
    GROUP BY c.id, c.title, c.difficulty_level, c.estimated_time_minutes, sc.name, cat.name
    ORDER BY cat.sort_order, sc.sort_order, c.title
    LIMIT p_limit OFFSET p_offset;
    
    COMMIT;
END //

DELIMITER ;
```

#### Views بهینه
```sql
-- View برای آمار سریع
CREATE VIEW v_case_summary AS
SELECT 
    cat.id AS category_id,
    cat.name AS category_name,
    sc.id AS subcategory_id,
    sc.name AS subcategory_name,
    COUNT(c.id) AS total_cases,
    SUM(CASE WHEN c.difficulty_level = 'beginner' THEN 1 ELSE 0 END) AS beginner_cases,
    SUM(CASE WHEN c.difficulty_level = 'intermediate' THEN 1 ELSE 0 END) AS intermediate_cases,
    SUM(CASE WHEN c.difficulty_level = 'advanced' THEN 1 ELSE 0 END) AS advanced_cases,
    AVG(c.estimated_time_minutes) AS avg_time_minutes
FROM category cat
JOIN sub_category sc ON cat.id = sc.category_id
LEFT JOIN case_study c ON sc.id = c.sub_category_id AND c.is_active = TRUE
WHERE cat.is_active = TRUE AND sc.is_active = TRUE
GROUP BY cat.id, cat.name, sc.id, sc.name;
```

## 📈 مانیتورینگ و Analytics

### 1. جداول Analytics
```sql
-- جدول آمار عملکرد
CREATE TABLE performance_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4),
    metric_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_metric_date (metric_date),
    INDEX idx_metric_name (metric_name)
);

-- جدول لاگ کوئری‌های کند
CREATE TABLE slow_query_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query_text TEXT,
    execution_time DECIMAL(10,4),
    rows_examined INT,
    rows_sent INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_execution_time (execution_time),
    INDEX idx_created_at (created_at)
);
```

### 2. کوئری‌های مانیتورینگ
```sql
-- بررسی ایندکس‌های استفاده نشده
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    CARDINALITY
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'veterinary_cases'
AND CARDINALITY = 0;

-- بررسی جداول بزرگ
SELECT 
    TABLE_NAME,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS 'Size (MB)',
    TABLE_ROWS
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'veterinary_cases'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- آمار کوئری‌های کند
SELECT 
    DATE(created_at) AS query_date,
    COUNT(*) AS slow_queries,
    AVG(execution_time) AS avg_execution_time,
    MAX(execution_time) AS max_execution_time
FROM slow_query_log
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY query_date DESC;
```

## 🔒 امنیت و Backup

### 1. Backup Strategy
```bash
#!/bin/bash
# اسکریپت Backup خودکار

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/veterinary_cases"
DB_NAME="veterinary_cases"

# ایجاد Backup کامل
mysqldump --single-transaction --routines --triggers \
    --user=backup_user --password=backup_pass \
    $DB_NAME > $BACKUP_DIR/full_backup_$DATE.sql

# فشرده‌سازی
gzip $BACKUP_DIR/full_backup_$DATE.sql

# حذف فایل‌های قدیمی (بیش از 30 روز)
find $BACKUP_DIR -name "full_backup_*.sql.gz" -mtime +30 -delete

# Backup جداول مهم جداگانه
mysqldump --single-transaction \
    --user=backup_user --password=backup_pass \
    $DB_NAME case_study case_test case_option > $BACKUP_DIR/critical_tables_$DATE.sql
```

### 2. امنیت داده
```sql
-- رمزنگاری داده‌های حساس
CREATE TABLE user_encrypted (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role ENUM('student', 'instructor', 'admin') DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- رمزنگاری فیلدهای حساس
    encrypted_data BLOB,
    INDEX idx_user_email (email),
    INDEX idx_user_active (is_active),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- محدودیت‌های دسترسی
CREATE USER 'app_user'@'%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON veterinary_cases.* TO 'app_user'@'%';
GRANT DELETE ON veterinary_cases.user_progress TO 'app_user'@'%';

CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON veterinary_cases.* TO 'readonly_user'@'%';
```

## 🚀 پیشنهادات برای رشد

### 1. Microservices Architecture
```yaml
# docker-compose.yml برای معماری میکروسرویس
version: '3.8'
services:
  database:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: veterinary_cases
    volumes:
      - ./database_schema.sql:/docker-entrypoint-initdb.d/init.sql
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: ./api
    depends_on:
      - database
      - redis
    environment:
      DB_HOST: database
      REDIS_HOST: redis
    ports:
      - "8000:8000"

volumes:
  mysql_data:
```

### 2. CDN برای تصاویر
```sql
-- جدول برای مدیریت فایل‌ها
CREATE TABLE file_assets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_test_id INT,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT,
    mime_type VARCHAR(100),
    cdn_url VARCHAR(500),
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_test_id) REFERENCES case_test(id) ON DELETE CASCADE,
    INDEX idx_file_processed (is_processed),
    INDEX idx_file_type (mime_type)
);
```

### 3. API Rate Limiting
```sql
-- جدول برای Rate Limiting
CREATE TABLE api_rate_limits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    endpoint VARCHAR(100),
    request_count INT DEFAULT 1,
    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_endpoint_window (user_id, endpoint, window_start),
    INDEX idx_window_start (window_start)
);
```

## 📊 معیارهای عملکرد

### KPIs مهم
- **Query Response Time**: < 100ms برای 95% کوئری‌ها
- **Database Uptime**: > 99.9%
- **Cache Hit Rate**: > 80%
- **Backup Success Rate**: 100%
- **Data Growth**: < 10GB در ماه

### ابزارهای مانیتورینگ
- **MySQL Enterprise Monitor**
- **Percona Monitoring and Management**
- **Prometheus + Grafana**
- **New Relic Database Monitoring**

---

**نکته**: این راهنما برای پایگاه داده‌های با حجم متوسط تا بالا طراحی شده است. برای پروژه‌های کوچک، می‌توانید بخش‌های مربوط به Sharding و Read Replicas را نادیده بگیرید. 
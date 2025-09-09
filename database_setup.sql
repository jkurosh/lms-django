-- =====================================================
-- Veterinary Cases Database Setup
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS veterinary_cases CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE veterinary_cases;

-- Categories table (e.g., "Internal Diseases", "Surgery")
CREATE TABLE category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_active (is_active),
    INDEX idx_category_sort (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Subcategories table (e.g., "Gastrointestinal", "Cardiovascular")
CREATE TABLE IF NOT EXISTS sub_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE,
    UNIQUE KEY uk_subcategory_name (category_id, name),
    INDEX idx_subcategory_active (is_active),
    INDEX idx_subcategory_sort (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Cases table (individual case studies)
CREATE TABLE IF NOT EXISTS case_study (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sub_category_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    patient_history TEXT NOT NULL,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'intermediate',
    estimated_time_minutes INT DEFAULT 15,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sub_category_id) REFERENCES sub_category(id) ON DELETE CASCADE,
    INDEX idx_case_active (is_active),
    INDEX idx_case_difficulty (difficulty_level),
    INDEX idx_case_subcategory (sub_category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Diagnostic tests for each case
CREATE TABLE IF NOT EXISTS case_test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_study_id INT NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    test_description TEXT,
    test_result TEXT,
    image_url VARCHAR(500),
    image_alt_text VARCHAR(255),
    sort_order INT DEFAULT 0,
    is_required BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (case_study_id) REFERENCES case_study(id) ON DELETE CASCADE,
    INDEX idx_test_case (case_study_id),
    INDEX idx_test_sort (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Answer options for each case
CREATE TABLE IF NOT EXISTS case_option (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_study_id INT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    explanation_hint VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (case_study_id) REFERENCES case_study(id) ON DELETE CASCADE,
    INDEX idx_option_case (case_study_id),
    INDEX idx_option_correct (is_correct),
    INDEX idx_option_sort (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Explanatory answer for each case
CREATE TABLE IF NOT EXISTS case_explanation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_study_id INT NOT NULL UNIQUE,
    explanation_text TEXT NOT NULL,
    key_learning_points TEXT,
    `references` TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (case_study_id) REFERENCES case_study(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- User Management (for future extensions)
-- =====================================================

-- Users table for future authentication and progress tracking
CREATE TABLE IF NOT EXISTS user (
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
    INDEX idx_user_email (email),
    INDEX idx_user_active (is_active),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User progress tracking (optional for future use)
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    case_study_id INT NOT NULL,
    selected_option_id INT,
    is_correct BOOLEAN,
    time_spent_seconds INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (case_study_id) REFERENCES case_study(id) ON DELETE CASCADE,
    FOREIGN KEY (selected_option_id) REFERENCES case_option(id) ON DELETE SET NULL,
    UNIQUE KEY uk_user_case (user_id, case_study_id),
    INDEX idx_progress_user (user_id),
    INDEX idx_progress_case (case_study_id),
    INDEX idx_progress_completed (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Sample Data Insertion
-- =====================================================

-- Insert sample categories
INSERT INTO category (name, description, sort_order) VALUES
('Internal Diseases', 'Cases related to internal medicine and systemic diseases', 1),
('Surgery', 'Surgical cases and procedures', 2),
('Emergency Medicine', 'Emergency and critical care cases', 3),
('Dermatology', 'Skin and coat related conditions', 4),
('Radiology', 'Imaging and diagnostic cases', 5);

-- Insert sample subcategories
INSERT INTO sub_category (category_id, name, description, sort_order) VALUES
(1, 'Gastrointestinal', 'Digestive system disorders', 1),
(1, 'Cardiovascular', 'Heart and circulatory system', 2),
(1, 'Respiratory', 'Lung and airway conditions', 3),
(2, 'Soft Tissue Surgery', 'Non-orthopedic surgical procedures', 1),
(2, 'Orthopedic Surgery', 'Bone and joint surgery', 2),
(3, 'Trauma', 'Accident and injury cases', 1),
(3, 'Toxicology', 'Poisoning and toxic exposure', 2);

-- Insert sample case
INSERT INTO case_study (sub_category_id, title, patient_history, difficulty_level, estimated_time_minutes) VALUES
(1, 'Acute Vomiting in a 3-year-old Golden Retriever', 'Max is a 3-year-old male Golden Retriever presenting with acute onset vomiting for the past 12 hours. The owner reports that Max has been lethargic and has not eaten since yesterday morning. There is no known history of dietary indiscretion or toxin exposure. Physical examination reveals mild dehydration and abdominal discomfort.', 'intermediate', 20);

-- Insert sample tests for the case
INSERT INTO case_test (case_study_id, test_name, test_description, test_result, sort_order) VALUES
(1, 'Complete Blood Count (CBC)', 'Routine blood work to assess for infection, inflammation, or anemia', 'WBC: 18,500/μL (normal: 4,000-15,500), Neutrophils: 85%, Lymphocytes: 10%', 1),
(1, 'Serum Chemistry Panel', 'Assessment of organ function and electrolyte balance', 'BUN: 45 mg/dL (normal: 7-27), Creatinine: 2.1 mg/dL (normal: 0.5-1.8), ALT: 180 U/L (normal: 10-100)', 2),
(1, 'Abdominal Radiographs', 'Survey radiographs to assess for foreign body or obstruction', 'No obvious foreign body visible. Mild gas distention in small intestine.', 3);

-- Insert sample options
INSERT INTO case_option (case_study_id, option_text, is_correct, sort_order) VALUES
(1, 'Gastric foreign body obstruction', FALSE, 1),
(1, 'Acute pancreatitis', TRUE, 2),
(1, 'Parvovirus infection', FALSE, 3),
(1, 'Addison''s disease', FALSE, 4);

-- Insert sample explanation
INSERT INTO case_explanation (case_study_id, explanation_text, key_learning_points) VALUES
(1, 'This case represents acute pancreatitis in a dog. The elevated WBC count with neutrophilia indicates inflammation, while the elevated BUN and creatinine suggest dehydration and potential kidney involvement. The elevated ALT indicates liver enzyme leakage, which is common in pancreatitis due to the close anatomical relationship between the pancreas and liver. The abdominal discomfort and vomiting are classic signs of pancreatitis. Treatment would include fluid therapy, anti-emetics, pain management, and withholding food for 24-48 hours followed by a low-fat diet.', 'Key learning points: 1. Pancreatitis should be considered in any dog with acute vomiting and abdominal pain 2. Elevated liver enzymes can occur secondary to pancreatitis 3. Dehydration is common and requires aggressive fluid therapy 4. Early diagnosis and treatment improve prognosis');

-- =====================================================
-- Additional Indexes for Performance
-- =====================================================

-- Composite indexes for common query patterns
CREATE INDEX idx_case_study_subcategory_active ON case_study(sub_category_id, is_active);
CREATE INDEX idx_case_test_case_sort ON case_test(case_study_id, sort_order);
CREATE INDEX idx_case_option_case_correct ON case_option(case_study_id, is_correct);
CREATE INDEX idx_user_progress_user_completed ON user_progress(user_id, completed_at);

-- =====================================================
-- Views for Common Queries
-- =====================================================

-- View for case details with category hierarchy
CREATE VIEW case_details AS
SELECT 
    c.id, c.title, c.patient_history, c.difficulty_level, c.estimated_time_minutes,
    sc.name AS subcategory_name, cat.name AS category_name, c.created_at
FROM case_study c
JOIN sub_category sc ON c.sub_category_id = sc.id
JOIN category cat ON sc.category_id = cat.id
WHERE c.is_active = TRUE;

-- View for case statistics
CREATE VIEW case_statistics AS
SELECT 
    c.id, c.title,
    COUNT(ct.id) AS test_count,
    COUNT(co.id) AS option_count,
    SUM(CASE WHEN co.is_correct = TRUE THEN 1 ELSE 0 END) AS correct_options
FROM case_study c
LEFT JOIN case_test ct ON c.id = ct.case_study_id
LEFT JOIN case_option co ON c.id = co.case_study_id
WHERE c.is_active = TRUE
GROUP BY c.id, c.title;

-- =====================================================
-- Stored Procedures for Common Operations
-- =====================================================

DELIMITER //

-- Procedure to get complete case with all related data
CREATE PROCEDURE GetCaseWithDetails(IN case_id INT)
BEGIN
    SELECT c.*, sc.name AS subcategory_name, cat.name AS category_name
    FROM case_study c
    JOIN sub_category sc ON c.sub_category_id = sc.id
    JOIN category cat ON sc.category_id = cat.id
    WHERE c.id = case_id AND c.is_active = TRUE;
    
    SELECT * FROM case_test WHERE case_study_id = case_id ORDER BY sort_order;
    SELECT * FROM case_option WHERE case_study_id = case_id ORDER BY sort_order;
    SELECT * FROM case_explanation WHERE case_study_id = case_id;
END //

-- Procedure to get cases by category
CREATE PROCEDURE GetCasesByCategory(IN category_id INT)
BEGIN
    SELECT c.*, sc.name AS subcategory_name
    FROM case_study c
    JOIN sub_category sc ON c.sub_category_id = sc.id
    WHERE sc.category_id = category_id AND c.is_active = TRUE
    ORDER BY sc.sort_order, c.title;
END //

DELIMITER ;

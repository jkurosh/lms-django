-- PostgreSQL schema for vetlms
-- Creates core tables: categories, sub_categories, case_studies, case_tests,
-- case_options, case_explanations, users, user_progress

BEGIN;

-- Optional useful extensions
CREATE EXTENSION IF NOT EXISTS citext;

-- Updated-at trigger helper
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =========================
-- Taxonomy
-- =========================
CREATE TABLE IF NOT EXISTS categories (
  id           BIGSERIAL PRIMARY KEY,
  name         TEXT NOT NULL UNIQUE,
  slug         TEXT UNIQUE,
  description  TEXT,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER trg_categories_updated_at
BEFORE UPDATE ON categories
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS sub_categories (
  id            BIGSERIAL PRIMARY KEY,
  category_id   BIGINT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
  name          TEXT NOT NULL,
  slug          TEXT,
  description   TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (category_id, name)
);

CREATE INDEX IF NOT EXISTS idx_sub_categories_category_id
  ON sub_categories(category_id);

CREATE TRIGGER trg_sub_categories_updated_at
BEFORE UPDATE ON sub_categories
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- =========================
-- Users
-- =========================
CREATE TABLE IF NOT EXISTS users (
  id                    BIGSERIAL PRIMARY KEY,
  full_name             TEXT,
  email                 CITEXT UNIQUE,
  phone_number          VARCHAR(20) UNIQUE,
  password_hash         TEXT NOT NULL,
  is_active             BOOLEAN NOT NULL DEFAULT TRUE,
  role                  VARCHAR(20) NOT NULL DEFAULT 'student',
  subscription_start    TIMESTAMPTZ,
  subscription_end      TIMESTAMPTZ,
  last_login            TIMESTAMPTZ,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_subscription_range CHECK (
    subscription_end IS NULL OR subscription_start IS NULL OR subscription_end >= subscription_start
  )
);

CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_subscription_window ON users(subscription_start, subscription_end);

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- =========================
-- Cases
-- =========================
CREATE TABLE IF NOT EXISTS case_studies (
  id               BIGSERIAL PRIMARY KEY,
  category_id      BIGINT REFERENCES categories(id) ON DELETE RESTRICT,
  sub_category_id  BIGINT REFERENCES sub_categories(id) ON DELETE RESTRICT,
  title            TEXT NOT NULL,
  slug             TEXT UNIQUE,
  summary          TEXT,
  difficulty       SMALLINT, -- 1..5
  tags             TEXT[],
  is_published     BOOLEAN NOT NULL DEFAULT FALSE,
  published_at     TIMESTAMPTZ,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_case_difficulty CHECK (difficulty IS NULL OR (difficulty >= 1 AND difficulty <= 5))
);

CREATE INDEX IF NOT EXISTS idx_case_studies_category ON case_studies(category_id);
CREATE INDEX IF NOT EXISTS idx_case_studies_sub_category ON case_studies(sub_category_id);
CREATE INDEX IF NOT EXISTS idx_case_studies_published ON case_studies(is_published, published_at);

CREATE TRIGGER trg_case_studies_updated_at
BEFORE UPDATE ON case_studies
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS case_tests (
  id              BIGSERIAL PRIMARY KEY,
  case_study_id   BIGINT NOT NULL REFERENCES case_studies(id) ON DELETE CASCADE,
  question        TEXT NOT NULL,
  type            VARCHAR(50) NOT NULL,
  order_index     INTEGER NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_case_test_type CHECK (type IN ('single_choice','multiple_choice','text','numeric'))
);

CREATE INDEX IF NOT EXISTS idx_case_tests_case_study_order
  ON case_tests(case_study_id, order_index);

CREATE TRIGGER trg_case_tests_updated_at
BEFORE UPDATE ON case_tests
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS case_options (
  id              BIGSERIAL PRIMARY KEY,
  case_test_id    BIGINT NOT NULL REFERENCES case_tests(id) ON DELETE CASCADE,
  option_text     TEXT NOT NULL,
  is_correct      BOOLEAN NOT NULL DEFAULT FALSE,
  explanation     TEXT,
  order_index     INTEGER NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_case_options_test_order
  ON case_options(case_test_id, order_index);

CREATE TRIGGER trg_case_options_updated_at
BEFORE UPDATE ON case_options
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE IF NOT EXISTS case_explanations (
  id              BIGSERIAL PRIMARY KEY,
  case_study_id   BIGINT NOT NULL REFERENCES case_studies(id) ON DELETE CASCADE,
  content         TEXT NOT NULL,
  media_url       TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_case_explanations_case
  ON case_explanations(case_study_id);

CREATE TRIGGER trg_case_explanations_updated_at
BEFORE UPDATE ON case_explanations
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- =========================
-- Progress Tracking
-- =========================
CREATE TABLE IF NOT EXISTS user_progress (
  id               BIGSERIAL PRIMARY KEY,
  user_id          BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  case_study_id    BIGINT NOT NULL REFERENCES case_studies(id) ON DELETE CASCADE,
  completed        BOOLEAN NOT NULL DEFAULT FALSE,
  score            NUMERIC(5,2),
  attempts         INTEGER NOT NULL DEFAULT 0,
  started_at       TIMESTAMPTZ,
  completed_at     TIMESTAMPTZ,
  last_test_id     BIGINT REFERENCES case_tests(id) ON DELETE SET NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, case_study_id)
);

CREATE INDEX IF NOT EXISTS idx_user_progress_user
  ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_case
  ON user_progress(case_study_id);

CREATE TRIGGER trg_user_progress_updated_at
BEFORE UPDATE ON user_progress
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMIT;



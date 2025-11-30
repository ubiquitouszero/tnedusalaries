CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rank TEXT,
    organization TEXT,
    department TEXT,
    salary REAL,
    year INTEGER,
    source TEXT, -- 'TN Tech', 'UT System'
    original_source_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_salaries_name ON salaries(name);
CREATE INDEX IF NOT EXISTS idx_salaries_year ON salaries(year);
CREATE INDEX IF NOT EXISTS idx_salaries_org ON salaries(organization);

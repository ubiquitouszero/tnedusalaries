# TN Tech Salary Analysis

A data-driven effort to understand Tennessee Tech faculty and staff compensation, benchmark against peer institutions, and build a business case for salary equity adjustments.

## Purpose

This project aggregates historical salary data from multiple sources to:

- Track TN Tech salary trends over the past 10+ years
- Compare compensation against peer institutions and CUPA benchmarks
- Identify salary compression and equity gaps
- Support evidence-based proposals for salary adjustments

## Data Sources

| Source | Type | Coverage |
|--------|------|----------|
| TN Tech Budget PDFs | Primary | FY2008-2026 budget summaries |
| UT System Dashboard | Peer comparison | Current employee salaries |
| IPEDS | National benchmarks | Historical faculty salary data |
| CUPA-HR | Industry benchmarks | Position-based salary surveys |

## Project Structure

```
tnedusalaries/
├── scrapers/                  # Data collection scripts
│   ├── tn_tech_download.py    # Download TN Tech budget PDFs
│   ├── tn_tech_parse.py       # Extract salary data from PDFs
│   └── ut_system_manual.md    # Manual extraction guide for UT data
├── data/                      # Raw data files (not tracked in git)
│   └── pdfs/                  # Downloaded budget PDFs
├── schema.sql                 # Database schema
├── init_db.py                 # Initialize SQLite database
├── salary_db.sqlite           # Salary data (SQLite)
├── verify_data.py             # Data validation utilities
├── generate_salary_graph.py   # Visualization scripts
└── tntech_*.html              # Analysis reports and dashboards
```

## Database Schema

```sql
CREATE TABLE salaries (
    id INTEGER PRIMARY KEY,
    name TEXT,
    rank TEXT,
    organization TEXT,
    department TEXT,
    salary REAL,
    year INTEGER,
    source TEXT,
    original_source_url TEXT,
    created_at DATETIME
);
```

## Quick Start

```bash
# Initialize the database
python init_db.py

# Download TN Tech budget PDFs
python scrapers/tn_tech_download.py

# Parse and import salary data
python scrapers/tn_tech_parse.py

# Generate visualizations
python generate_salary_graph.py
```

## Analysis Reports

- `tntech_salary_benchmarks.html` - CUPA benchmark comparisons
- `tntech_salary_analysis.html` - Historical trend analysis
- `tntech_merit_equity_framework.html` - Merit and equity framework proposal

## Data Privacy

This project uses publicly available salary data from state university budget documents and open records. Individual salary records are public information under Tennessee law.

## Contributing

Data contributions welcome, particularly:
- Historical budget documents
- Peer institution salary data
- IPEDS/CUPA benchmark datasets

## License

This project is for research and advocacy purposes.

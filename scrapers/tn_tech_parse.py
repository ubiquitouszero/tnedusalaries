import os
import sqlite3
import re
import sys

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed. Please install it using 'pip install pdfplumber'.")
    sys.exit(1)

DB_PATH = "salary_db.sqlite"
PDF_DIR = os.path.join("data", "pdfs")

def parse_pdf(filepath, year):
    print(f"Parsing {filepath} for year {year}...")
    extracted_data = []
    
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            # pdfplumber's extract_table is powerful but needs tuning.
            # We'll try default settings first, then maybe text-based if that fails.
            
            # Strategy 1: Extract text line by line (pdfplumber handles layout better than pypdf)
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            for line in lines:
                # Regex for: Name ... Rank ... Dept ... Salary
                # Example: "Smith, John   Professor   Chemistry   $100,000"
                # We look for the salary at the end.
                
                # Salary pattern: $? followed by digits/commas, at end of line
                # We also want to capture the name at the start.
                
                # Regex breakdown:
                # ^(.+?)          - Capture start (Name + other stuff) non-greedy
                # \s+             - Separator
                # \$?([0-9,]+)    - Capture Salary (digits and commas)
                # (\.[0-9]{2})?   - Optional cents
                # $               - End of line
                
                match = re.search(r'^(.+?)\s+\$?([0-9,]{4,})(\.[0-9]{2})?$', line)
                if match:
                    content_part = match.group(1).strip()
                    salary_str = match.group(2).replace(',', '')
                    
                    try:
                        salary = float(salary_str)
                    except ValueError:
                        continue
                        
                    # Filter out page numbers, years, totals
                    if salary < 15000: # Minimum wage/part time filter
                        continue
                    if "Total" in content_part or "Page" in content_part or "Budget" in content_part:
                        continue
                        
                    # Heuristic to split Name / Rank / Dept
                    # We assume Name is first.
                    # If we have multiple spaces, we can try to split.
                    parts = re.split(r'\s{2,}', content_part)
                    
                    name = parts[0]
                    rank = parts[1] if len(parts) > 1 else ""
                    dept = parts[2] if len(parts) > 2 else ""
                    
                    # Clean up name (remove leading numbers/codes if any)
                    name = re.sub(r'^\d+\s+', '', name)
                    
                    extracted_data.append((name, rank, "TN Tech", dept, salary, year, "TN Tech PDF"))

    return extracted_data

def save_to_db(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Use INSERT OR IGNORE or replace to avoid duplicates if re-running
    c.executemany('''
        INSERT INTO salaries (name, rank, organization, department, salary, year, source, original_source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(d[0], d[1], d[2], d[3], d[4], d[5], d[6], "PDF") for d in data])
    conn.commit()
    conn.close()
    print(f"Saved {len(data)} records.")

def main():
    files = os.listdir(PDF_DIR)
    for f in files:
        if not f.endswith(".pdf"):
            continue
            
        year_match = re.search(r'20(\d{2})', f)
        if year_match:
            year = int("20" + year_match.group(1))
            
            # Prioritize "Analysis" or "Summary" files that look like detailed lists
            if "Analysis" in f or "Summary" in f:
                path = os.path.join(PDF_DIR, f)
                try:
                    data = parse_pdf(path, year)
                    if data:
                        save_to_db(data)
                except Exception as e:
                    print(f"Failed to parse {f}: {e}")

if __name__ == "__main__":
    main()

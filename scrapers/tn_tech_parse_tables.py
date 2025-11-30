import os
import sqlite3
import pdfplumber
import re

DB_PATH = "salary_db.sqlite"
PDF_DIR = os.path.join("data", "pdfs")

def parse_pdf_tables(filepath, year):
    print(f"Parsing tables from {filepath} for year {year}...")
    extracted_data = []
    
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            # Try to extract tables directly
            tables = page.extract_tables()
            
            for table in tables:
                for row in table:
                    # Clean row data
                    # We expect a row to have Name, Rank, Dept, Salary in some order.
                    # Usually: Name, Title, Dept, Salary
                    # Or: Index, Name, Title, Salary...
                    
                    # Filter out None or empty strings
                    row = [str(x).strip() for x in row if x]
                    
                    if not row:
                        continue
                        
                    # Heuristic: Find the salary field (looks like money)
                    salary_idx = -1
                    salary = 0.0
                    
                    for i, cell in enumerate(row):
                        # Check for money format: $100,000 or 100,000.00
                        # Must have at least 4 digits to be a salary we care about (>1000)
                        if re.match(r'^\$?[0-9,]+\.?[0-9]*$', cell):
                            try:
                                val = float(cell.replace('$', '').replace(',', ''))
                                if val > 10000: # Salary threshold
                                    salary = val
                                    salary_idx = i
                                    break
                            except ValueError:
                                continue
                    
                    if salary_idx != -1:
                        # If we found a salary, try to identify Name and Rank
                        # Usually Name is the first non-numeric text field
                        
                        name = ""
                        rank = ""
                        dept = ""
                        
                        # Get text fields before salary
                        text_fields = []
                        for i in range(salary_idx):
                            if re.search(r'[A-Za-z]', row[i]): # Has letters
                                text_fields.append(row[i])
                                
                        if len(text_fields) >= 1:
                            name = text_fields[0]
                        if len(text_fields) >= 2:
                            rank = text_fields[1]
                        if len(text_fields) >= 3:
                            dept = text_fields[2]
                            
                        # Clean name (remove "123456 " index if present)
                        name = re.sub(r'^\d+\s+', '', name)
                        
                        if name and "Total" not in name and "Budget" not in name:
                            extracted_data.append((name, rank, "TN Tech", dept, salary, year, "TN Tech PDF Table"))

    return extracted_data

def save_to_db(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
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
            
            # Only process if it's a likely data file
            if "Analysis" in f or "Summary" in f:
                path = os.path.join(PDF_DIR, f)
                try:
                    data = parse_pdf_tables(path, year)
                    if data:
                        save_to_db(data)
                    else:
                        print(f"No table data found in {f}")
                except Exception as e:
                    print(f"Failed to parse {f}: {e}")

if __name__ == "__main__":
    main()

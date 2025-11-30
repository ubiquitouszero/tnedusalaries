import sqlite3
import pandas as pd

DB_PATH = "salary_db.sqlite"

def verify():
    conn = sqlite3.connect(DB_PATH)
    
    # Count total records
    count = pd.read_sql_query("SELECT COUNT(*) as count FROM salaries", conn)
    print(f"Total records: {count['count'][0]}")
    
    # Count by year
    by_year = pd.read_sql_query("SELECT year, COUNT(*) as count FROM salaries GROUP BY year ORDER BY year", conn)
    print("\nRecords by Year:")
    print(by_year)
    
    # Show sample
    print("\nSample Data:")
    sample = pd.read_sql_query("SELECT * FROM salaries ORDER BY RANDOM() LIMIT 5", conn)
    print(sample)
    
    conn.close()

if __name__ == "__main__":
    verify()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Connect to database
conn = sqlite3.connect('salary_db.sqlite')

# Query data
query = """
SELECT year, AVG(salary) as avg_salary
FROM salaries
WHERE salary > 0
GROUP BY year
ORDER BY year
"""

try:
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("No data found in database to plot.")
    else:
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['year'], df['avg_salary'], marker='o')
        plt.title('Average Salary by Year')
        plt.xlabel('Year')
        plt.ylabel('Average Salary ($)')
        plt.grid(True)
        
        # Save plot
        output_file = 'salary_trend.png'
        plt.savefig(output_file)
        print(f"Graph saved to {os.path.abspath(output_file)}")
        
except Exception as e:
    print(f"Error generating graph: {e}")
finally:
    conn.close()

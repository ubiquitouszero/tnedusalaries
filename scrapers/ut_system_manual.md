# UT System Salary Data Extraction

The UT System data is hosted on a Power BI dashboard at [data.tennessee.edu](https://data.tennessee.edu/).
Automated extraction is difficult due to the lack of a public API and the dynamic nature of the dashboard.

## Manual Extraction Steps

1.  Visit [UT System Employee Salaries Dashboard](https://data.tennessee.edu/).
2.  Navigate to the "Human Resources" section and select "Employee Salaries".
3.  Use the filters to select the desired year (if available) or view the current snapshot.
4.  If an "Export" option is available (often under the "..." menu on the table visual), export the data to CSV.
5.  Save the CSV to `data/ut_system_salaries.csv`.
6.  Run the importer script (to be created) to load this CSV into the SQLite database.

## Alternative
If "seekUT" provides a better data download, use that source. However, seekUT is primarily for graduate earnings, not employee salaries.

# 20260817-Module5

I have created an app which takes two datasets for a library which contains customer data and loaned book data and cleans it to remove duplicates, nulls and date errors before exporting them as csvs to be loaded into Power BI.

Here is a summary of the cleaning steps and how many rows were removed from each dataset.
![Pipeline Architecture Diagram](images\cleaning_summary.png)

## Output Files Summary

| `loan_data_cleaned.csv` | Sanitized, validated, and duration-enriched book loan data. |
| `loan_errors.csv` | Quarantined rows where loan duration logic failed (`date_delta < 0`). |
| `loan_data_row_counts_summary.csv` | Step-by-step audit trail of row drops across the book cleaning lifecycle. |
| `customers_data_cleaned.csv` | Cleaned and deduplicated customer records. |
| `customers_row_counts_summary.csv` | Step-by-step audit trail of row drops across the customer cleaning lifecycle. |
| `log.txt` | Execution timestamp log tracking successful artifact generation. |
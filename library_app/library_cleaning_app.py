import pandas as pd
from pathlib import Path
from datetime import datetime

# Function to output dataframe via a filepath
def fileLoader(filepath):
    return pd.read_csv(filepath)

# Cleaning functions
def duplicateCleaner(df):
    return df.drop_duplicates().reset_index(drop=True)

def naCleaner(df):
    return df.dropna().reset_index(drop=True)

def dateCleaner(col, df):
    df[col] = df[col].str.replace('"', "", regex=True)
    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
    except Exception as e:
        print(f"Error while converting column {col} to datetime: {e}")
    error_flag = df[col].isna()
    df = df[~error_flag].copy()
    df.reset_index(drop=True, inplace=True)
    return df

def enrich_dateDuration(colA, colB, df):
    df['date_delta'] = (df[colB] - df[colA]).dt.days
    error_flag = df['date_delta'] < 0
    date_delta_errors = df[error_flag].copy()
    df = df[~error_flag].reset_index(drop=True)
    return df, date_delta_errors

def run_cleaning_pipeline():
    clean_data_dir = Path("data") / "clean_data"
    clean_data_dir.mkdir(parents=True, exist_ok=True)
    out = Path("log.txt")

    # 1. Process Library Books
    book_path = Path("data") / "source_data" / "03_Library Systembook.csv"
    data = fileLoader(filepath=book_path)
    
    s_init = data.shape[0]
    data = duplicateCleaner(data)
    s_dup = data.shape[0]
    data = naCleaner(data)
    s_null = data.shape[0]
    
    for col in ['Book checkout', 'Book Returned']:
        data = dateCleaner(col, data)
    
    data, loan_errors = enrich_dateDuration(df=data, colA='Book Returned', colB='Book checkout')
    s_final = data.shape[0]
    
    loan_summary = pd.DataFrame({
        'Dataset': 'Loans',
        'Description': ['Initial Rows', 'Duplicates Removed', 'Nulls Removed', 'Loan Date Errors Removed', 'Final Row Count'],
        'Count': [s_init, s_init - s_dup, s_dup - s_null, s_null - s_final, s_final]
    })

    # 2. Process Library Customers
    cust_path = Path("data") / "source_data" / "03_Library SystemCustomers.csv"
    data2 = fileLoader(filepath=cust_path)
    
    c_init = data2.shape[0]
    data2 = duplicateCleaner(data2)
    c_dup = data2.shape[0]
    data2 = naCleaner(data2)
    c_null = data2.shape[0]
    
    cust_summary = pd.DataFrame({
        'Dataset': 'Customers',
        'Description': ['Initial Rows', 'Duplicates Removed', 'Nulls Removed', 'Loan Date Errors Removed', 'Final Row Count'],
        'Count': [c_init, c_init - c_dup, c_dup - c_null, "N/A", c_null]
    })

    # 3. Combine and Pivot Summaries
    combined_summary = pd.concat([loan_summary, cust_summary], ignore_index=True)
    
    # Pivot so Description is the row index, and Loans/Customers are columns
    pivoted_summary = combined_summary.pivot(index='Description', columns='Dataset', values='Count')
    
    # Ensure rows follow the intended logical order
    row_order = ['Initial Rows', 'Duplicates Removed', 'Nulls Removed', 'Loan Date Errors Removed', 'Final Row Count']
    pivoted_summary = pivoted_summary.reindex(row_order).reset_index()
    
    # Export Pivoted Summary
    pivoted_summary.to_csv(clean_data_dir / 'combined_cleaning_summary.csv', index=False)
    
    # Save cleaned files
    data.to_csv(clean_data_dir / 'loan_data_cleaned.csv', index=False)
    loan_errors.to_csv(clean_data_dir / 'loan_errors.csv', index=False)
    data2.to_csv(clean_data_dir / 'customers_data_cleaned.csv', index=False)

    # Write to log file
    with out.open("a") as f:
        f.write(f"combined_cleaning_summary.csv generated at [{datetime.now()}]\n")
    
    # Print completion message
    print("Cleaning pipeline completed successfully. Cleaned data and summary files are saved in the 'data/clean_data' directory.")

if __name__ == '__main__':
    run_cleaning_pipeline()
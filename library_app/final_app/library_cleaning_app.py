## Before starting, in terminal run 'pip install -r Requirements.txt'

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from datetime import datetime

# Function to output dataframe that can be manipulated via a filepath
def fileLoader(filepath):
    data = pd.read_csv(filepath)
    return data 

# Duplicate Dropping Function
def duplicateCleaner(df):
    return df.drop_duplicates().reset_index(drop=True)

# NA handler - future scope can handle errors more elegantly. 
def naCleaner(df):
    return df.dropna().reset_index(drop=True)

# Turning date columns into datetime
def dateCleaner(col, df):
    # Store rows with date errors
    date_errors = pd.DataFrame(columns=df.columns)  

    # Strip any quotes from dates
    df[col] = df[col].str.replace('"', "", regex=True)

    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

    except Exception as e:
        print(f"Error while converting column {col} to datetime: {e}")

    # Identify rows with invalid dates
    error_flag = pd.to_datetime(df[col], dayfirst=True, errors='coerce').isna()
        
    # Move invalid rows to date_errors
    date_errors = df[error_flag]
        
    # Keep only valid rows in df
    df = df[~error_flag].copy()

    # Reset index for the cleaned DataFrame
    df.reset_index(drop=True, inplace=True)

    return df

def enrich_dateDuration(colA, colB, df):
    """
    Takes the two datetime input column names and the dataframe to create a new column date_delta which is the difference, in days, between colA and colB.
    
    Note:
    colB>colA
    """
    df['date_delta'] = (df[colB]-df[colA]).dt.days

    #Conditional Filtering to be able to gauge eroneous loans.
    error_flag = df['date_delta'] < 0

    # Move invalid rows to date_errors
    date_delta_errors = df[error_flag].copy()
        
    # Keep only valid rows in df
    df = df[~error_flag]

    return df, date_delta_errors

if __name__ == '__main__':

    print('**************** Starting Clean ****************')

    # Generate log file path
    out = Path("log.txt")

    # Find parent directory
    script_dir = Path(__file__).resolve().parent

    # Get data from path
    date_columns = ['Book checkout', 'Book Returned']
    data = fileLoader(filepath=script_dir.parent / 'data' / '03_Library Systembook.csv')

    # Drop duplicates & NAs
    Systembook_initial_rows = data.shape[0]
    data = duplicateCleaner(data)
    Systembook_deduplicated_rows = data.shape[0]
    data = naCleaner(data)
    Systembook_nulls_removed_rows = data.shape[0]

    # Converting date columns into datetime
    for col in date_columns:
        data = dateCleaner(col, data)
    
    # Enriching the dataset
    data, loan_errors = enrich_dateDuration(df=data, colA='Book Returned', colB='Book checkout')
    Systembook_loan_errors_rows = data.shape[0]
    
    # After cleaning steps, define the row counts in a dictionary
    loan_data_row_counts_summary = {
        'Description': ['Initial Rows', 'After Deduplication', 'After Removing Nulls', 'After Removing Loan Data Errors'],
        'Count': [Systembook_initial_rows, Systembook_deduplicated_rows, Systembook_nulls_removed_rows, Systembook_loan_errors_rows]
    }

    # Convert to DataFrame
    loan_data_row_counts_summary = pd.DataFrame(loan_data_row_counts_summary)

    # Export to CSV
    loan_data_row_counts_summary.to_csv(script_dir.parent / 'data' / 'loan_data_row_counts_summary.csv', index=False)

    # Export loan_data_cleaned
    data.to_csv(script_dir.parent / 'data' / 'loan_data_cleaned.csv', index=False)
    loan_errors.to_csv(script_dir.parent / 'data' / 'loan_errors.csv', index=False)

    # Write to log
    with out.open("a") as f:
        f.write(f"loan_data_cleaned.csv generated at [{datetime.now()}]\n")    

    #Cleaning the customer file
    data2 = fileLoader(filepath = script_dir.parent / 'data' / '03_Library SystemCustomers.csv')

    # Drop duplicates & NAs
    Customers_initial_rows = data2.shape[0]
    data2 = duplicateCleaner(data2)
    Customers_deduplicated_rows = data2.shape[0]
    data2 = naCleaner(data2)
    Customers_nulls_removed_rows = data2.shape[0]

    # After cleaning steps, define the row counts in a dictionary
    customers_row_counts_summary = {
        'Description': ['Initial Rows', 'After Deduplication', 'After Removing Nulls'],
        'Count': [Customers_initial_rows, Customers_deduplicated_rows, Customers_nulls_removed_rows]
    }

    # Convert to DataFrame
    customers_row_counts_summary = pd.DataFrame(customers_row_counts_summary)

    # Export to CSV
    customers_row_counts_summary.to_csv(script_dir.parent / 'data' / 'customers_row_counts_summary.csv', index=False)

    # Export customers_data_cleaned
    data2.to_csv(script_dir.parent / 'data' / 'customers_data_cleaned.csv', index=False)

    # Write to log
    with out.open("a") as f:
        f.write(f"customers_data_cleaned.csv generated at [{datetime.now()}]\n")

    print('**************** Data Cleaned ****************')

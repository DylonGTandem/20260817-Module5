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


# Get error date_delta
def error_date_delta(colA,df):
    """
    Takes the two datetime input column names and the dataframe to create a new column date_delta which is the difference, in days, between colA and colB.
    
    Note:
    colB>colA
    """
    df['date_delta'] = (df[colB]-df[colA]).dt.days

    # Conditional Filtering to be able to gauge eroneous loans.
    error_flag = df['date_delta'] < 0

    # Keep the flag column
    df['valid_loan_flag'] = ~error_flag
    
    # Move invalid rows to date_errors
    date_delta_errors = df[error_flag].copy()

    return date_delta_errors

if __name__ == '__main__':
    print('**************** Starting Clean ****************')

    # Instantiation
    dropCount= 0
    customer_drop_count = 0

    # Find parent directory
    script_dir = Path(__file__).resolve().parent

    # Get data from path
    date_columns = ['Book checkout', 'Book Returned']
    data = fileLoader(filepath=script_dir.parent / 'data' / '03_Library Systembook.csv')

    # Drop duplicates & NAs
    data = duplicateCleaner(data)
    data = naCleaner(data)

    # Converting date columns into datetime
    for col in date_columns:
        data = dateCleaner(col, data)
    
    # Enriching the dataset, removing invalid loans
    data = enrich_dateDuration(df=data, colA='Book Returned', colB='Book checkout')

    # Generate log file path
    out = Path("log.txt")

    print(data)

    # Export loan_data_cleaned
    data.to_csv(script_dir.parent / 'data' / 'loan_data_cleaned.csv', index=False)

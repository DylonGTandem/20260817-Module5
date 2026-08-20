import unittest
import pandas as pd
from pathlib import Path
from datetime import datetime

def fileLoader(filepath):
    data = pd.read_csv(filepath)
    return data 

# Find parent directory
script_dir = Path(__file__).resolve().parent

# Get data 
loan_data = fileLoader(filepath = script_dir.parent / 'library_app' / 'data' / 'loan_data_cleaned.csv')

customer_data = fileLoader(filepath = script_dir.parent / 'library_app' / 'data' / 'customers_data_cleaned.csv')


class TestDataLoading(unittest.TestCase):
    def test_loan_data_not_empty(self):
        # Verify loan data loaded successfully
        self.assertFalse(loan_data.empty)

    def test_customer_data_not_empty(self):
        # Verify customer data loaded successfully
        self.assertFalse(customer_data.empty)

    def test_date_delta(self):
         #Verify date_delta >= 0
         self.assertTrue((loan_data['date_delta'] >= 0).all())

if __name__ == "__main__":
       '''
       # Generate log file path
       out = Path(script_dir.parent / 'library_app' / 'final_app' / 'log.txt')
       with out.open("a") as f:
        f.write(f"Library data tested at [{datetime.now()}]\n")
       '''
       unittest.main()
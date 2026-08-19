import unittest
import pandas as pd

def fileLoader(filepath):
    data = pd.read_csv(filepath)
    return data 

loan_data = fileLoader(filepath='loan_data_cleanedV2.csv')
customer_data = fileLoader(filepath='customers_data_cleanedV2.csv')

class TestDataLoading(unittest.TestCase):
    def test_load_datasets(self):
        # Verify data loaded successfully
        self.assertFalse(loan_data.empty)
        self.assertFalse(customer_data.empty)

    def test_date_delta(self):
         #Verify date_delta >= 0
         self.assertTrue(loan_data['date_delta'] >= 0)
'''
class TestOperation(unittest.TestCase):
    
        def test_sum(self):
              calculation = Calculator(8,2)
              answer = calculation.get_sum()
              self.assertEqual(answer,10,"The sum is wrong!")
        def test_diff(self):
              calculation = Calculator(8,2)
              answer = calculation.get_diff()
              self.assertEqual(answer,6,"The difference is wrong!")
        def test_product(self):
              calculation = Calculator(8,2)
              answer = calculation.get_product()
              self.assertEqual(answer,16,"The product is wrong!")
        def test_division(self):
              calculation = Calculator(8,2)
              answer = calculation.get_division()
              self.assertEqual(answer,4,"The division is wrong!")
'''
if __name__ == "__main__":
       unittest.main()

import unittest
from unittest.mock import patch
from StockAnalysisV1 import get_company_list,get_stock_history,get_choice
from PredictiveAnalyticsV1 import run_regression
from Input_ValidationV1 import input_period,input_date

class testStockquote(unittest.TestCase):
    def test_get_company_list(self):
        print("Test get_company_list")
        read_list = get_company_list()
        self.assertIsNotNone(read_list)
    
    def test_get_stock_history(self):
        print("Tesr get_stock_history")
        data = get_stock_history('amzn')
        self.assertIn('2021-09-01', data.index)
    
    def test_get_choice(self):
        print('Test get_choice')
        choice = get_choice()
        self.assertEqual('1', choice)
        
  
    def test_input_period(self):
        print('Test input period')
        period = input_period()
        self.assertEqual('3mo', period)
    
    def test_input_date(self):
        print('Test input data')
        start, end = input_date()
        self.assertEqual('2020-01-01', start)
        
        
if __name__ == '__main__':
    unittest.main()
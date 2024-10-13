import unittest

# from .. import ApplicationCore 
from AppCore.Models import TradingCard

class TradingCard_test(unittest.TestCase):
    def setUp(self) -> None:
        print("setup")
        return super().setUp()
    
    def tearDown(self) -> None:
        print("Tear down")
        return super().tearDown()
    
    def test_increment(self):
        pass

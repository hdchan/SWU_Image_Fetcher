import unittest   # The test framework
from Data.SWUDBClient import *

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(SWUDB_API_ENDPOINT, 'https://api.swu-db.com/cards/search')


if __name__ == '__main__':
    unittest.main()
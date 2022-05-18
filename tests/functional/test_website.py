#got testing info from https://www.youtube.com/watch?v=iQVvpnRYl-w


import unittest
import requests
from app import get_tasks


class WebsiteTestCase(unittest.TestCase):

    def test_home_page(self):
        r = requests.get('/get_tasks')
        self.assertEqual(r.status_code, 200)
        #self.assertTrue('<h4>BOOK LIST</h4>' in r.get_data(as_text=True)

if __name__ == "__main__":
    unittest.main()

import unittest
import requests
from app import get_tasks


class WebsiteTestCase(unittest.TestCase):

    def test_home_page(self):
        site_url = "https://djm-flask-book-review-test.herokuapp.com/" #works
        #site_url = "https://5000-djmolloy57-test18thaprp-3wxtq8uzxcn.ws-eu45.gitpod.io/"
        r = requests.get(site_url)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'<h4>BOOK LIST</h4>', r.data)
        #self.assertTrue('<h4>BOOK LIST</h4>' in r.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()

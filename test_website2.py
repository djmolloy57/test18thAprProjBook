import unittest
from app import app
from flask_pymongo import PyMongo

class TestOnlineBookStore(unittest.TestCase):

    # Ensure Flask app loads correctly
    def test_homepage(self):
        app.app_context
        client = app.test_client(self)
        response = client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h4>BOOK LIST</h4>', response.data)

    def test_scifi(self):
        app.app_context
        client = app.test_client(self)
        response = client.get('/get_scifi', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h4>SciFi Book List</h4>', response.data)


    def test_history(self):
        app.app_context
        client = app.test_client(self)
        response = client.get('/get_history', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h4>History Book List</h4>', response.data)

    
    

if __name__ == '__main__':
    unittest.main(verbosity=2)

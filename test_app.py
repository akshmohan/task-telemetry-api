import unittest
from unittest.mock import patch
from app.app import app

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # Changed 'redis_client' to 'cache' to match your app.py
    @patch('app.app.cache') 
    def test_health_endpoint(self, mock_redis):
        """Check if the root endpoint returns 200 without needing real Redis"""
        # Fake the redis 'incr' method (which your code uses)
        mock_redis.incr.return_value = 1
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
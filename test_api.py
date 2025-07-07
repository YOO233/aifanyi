import unittest
import requests
from dify_config import API_URL, API_KEY

class TestTranslationAPI(unittest.TestCase):
    def test_normal_translation(self):
        response = requests.post(
            API_URL,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                "inputs": {"content": "Hello world"},
                "response_mode": "blocking",
                "user": "test-user"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('data', data)
        self.assertIn('outputs', data['data'])

    def test_long_text(self):
        long_text = "a" * 5000  # 测试长文本处理
        response = requests.post(
            API_URL,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                "inputs": {"content": long_text},
                "response_mode": "blocking",
                "user": "stress-test"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_token(self):
        response = requests.post(
            API_URL,
            headers={
                'Authorization': 'Bearer invalid_token',
                'Content-Type': 'application/json'
            },
            json={
                "inputs": {"content": "test"},
                "response_mode": "blocking",
                "user": "test-user"
            }
        )
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()

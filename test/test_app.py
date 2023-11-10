import unittest
import json
from app import app, db, User
from flask_jwt_extended import create_access_token

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        # Configurations for the test environment
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['LIMITEr_ENABLED'] = False
        app.config['JWT_SECRET_KEY'] = 'test_jwt_secret_key'

        # Establish an application context before running the tests
        self.ctx = app.app_context()
        self.ctx.push()

        # Set up the Flask test client
        self.client = app.test_client()

        # Create tables and test user in the database
        with app.app_context():
            db.create_all()
            test_user = User(username='test', password_hash='test')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        # Cleanup and remove database session
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_home(self):
        # Test the home endpoint
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the API', response.get_data(as_text=True))

    def test_user_registration(self):
        # Test user registration
        response = self.client.post('/register', json={'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        # Test user login
        response = self.client.post('/login', json={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_shorten_url(self):
        # Test URL shortening
        # First, get a test JWT token for authentication
        test_token = create_access_token(identity='test')

        response = self.client.post(
            '/shorten', 
            json={'url': 'https://example.com'},
            headers={'Authorization': f'Bearer {test_token}'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('shortcode', json.loads(response.data))

    def test_redirect_to_url(self):
        # Test redirect from shortcode
        # This assumes you have a valid shortcode 'abc123' in the database
        response = self.client.get('/abc123')
        self.assertEqual(response.status_code, 200)

    # You can add more tests for rate limiting, invalid cases, etc.

if __name__ == '__main__':
    unittest.main()

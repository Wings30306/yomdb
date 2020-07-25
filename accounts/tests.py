from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class AccountsTests(TestCase):

    def test_homepage(self):
        """ Test that homepage is rendered """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """ Check that page redirects to secure site (https) """
        response = self.client.get('/accounts/login')
        self.assertEqual(response.status_code, 301)

    def test_logout(self):
        """ Test that user leaves secure zone on logging out """
        response = self.client.get('/accounts/logout')
        self.assertEqual(response.status_code, 301)
    
class UserModelTest(TestCase):
    def test_string_representation(self):
        """ Test admin side string representation of User instance """
        user = User(username="TestUser")
        self.assertEqual(str(user), user.username)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class UserRelatedTestCases(APITestCase):
    fixtures = []

    def test_register_user(self):
        """
        Test register user
        """
        url = reverse('register')
        response = self.client.post(
            url,
            {
                'first_name': 'Abhinav',
                'last_name': 'Dev',
                'email': 'theabhinavdev@gmail.com',
                'password': 'Password@123',
                'password2': 'Password@123',
                'username': 'theabhinav'
            },
            format='json'
        )
        self.assertEqual(response.status_code == 201, True)

    def test_login_user(self):
        """
        Test user login and authenticate as that user
        """
        url = reverse('login')
        self.test_register_user()
        response = self.client.post(
            url,
            {
                'password': 'Password@123',
                'username': 'theabhinav'
            },
            format='json'
        )
        self.assertEqual(response.status_code == 200, True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data.get('auth_token').get('access'))

    def test_logout(self):
        self.test_login_user()
        url = reverse('logout')
        response = self.client.post(
            url,
            format='json'
        )
        self.assertEqual(response.status_code == 200, True)

    def test_change_password(self):
        self.test_login_user()
        url = reverse('change_password')
        response = self.client.post(
            url,
            {
                'old_password': 'Password@123',
                'password': 'PASSWORD@123',
                'password2': 'PASSWORD@123'
            },
            format='json'
        )
        self.assertEqual(response.status_code == 200, True)

    def test_password_reset(self):
        url = reverse('password_reset:reset-password-request')
        self.test_register_user()
        response = self.client.post(
            url,
            {
                'email': 'theabhinavdev@gmail.com',
            },
            format='json'
        )
        self.assertEqual(response.status_code == 200, True)

    def test_update_profile(self):
        url = reverse('update_profile')
        self.test_login_user()
        response = self.client.post(
            url,
            {
                'email': 'theabhinavdev@gmail.com',
                'first_name': 'Some first name',
                'last_name': 'Some last name',
                'username': 'random123',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_get_profile(self):
        url = reverse('get_profile')
        self.test_login_user()
        response = self.client.get(
            url,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

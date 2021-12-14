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
                'first_name': 'Jeffrey',
                'last_name': 'Drum',
                'email': 'jeffrey@gaugedsolutions.com',
                'password': 'Password@123',
                'password2': 'Password@123',
                'username': 'JeffDrum'
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
                'username': 'JeffDrum'
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
                'email': 'jeffrey@gaugedsolutions.com',
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
                'email': 'jeffrey@gaugedsolutions.com',
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


class APIUserTestCases(APITestCase):
    def register_user(self):
        """
        register user
        """
        url = reverse('register')
        response = self.client.post(
            url,
            {
                'first_name': 'Jeffrey',
                'last_name': 'Drum',
                'email': 'jeffrey@gaugedsolutions.com',
                'password': 'Password@123',
                'password2': 'Password@123',
                'username': 'JeffDrum'
            },
            format='json'
        )
        self.assertEqual(response.status_code == 201, True)

    def login_user(self):
        """
         user login and authenticate as that user
        """
        self.register_user()
        url = reverse('login')
        response = self.client.post(
            url,
            {
                'password': 'Password@123',
                'username': 'JeffDrum'
            },
            format='json'
        )
        self.assertEqual(response.status_code == 200, True)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data.get('auth_token').get('access'))

    def test_api_user_creation(self):
        self.login_user()
        url = reverse('api_user-list')
        response = self.client.post(
            url,
            {
                'api_user_name': 'Some name',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_api_user_list(self):
        self.login_user()
        url = reverse('api_user-list')
        response = self.client.get(
            url,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_api_user_retrieve(self):
        self.test_api_user_creation()
        url = reverse('api_user-detail', args=[2])
        response = self.client.get(
            url,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_api_user_delete(self):
        self.test_api_user_creation()
        url = reverse('api_user-detail', args=[2])
        response = self.client.delete(
            url,
            format='json'
        )
        self.assertEqual(response.status_code, 204)

    def test_alter_user_validity(self):
        self.test_api_user_creation()
        url = reverse('alter_user_token')
        data_list = [
            {
                'user': 2,
                'action': action
            } for action in [
                'invalidate', 'validate', 'validate', 'invalidate'
            ]
        ]
        result = [True, True, False, True]
        for i in range(4):
            response = self.client.post(
                url,
                data=data_list[i],
                format='json'
            )
            self.assertEqual(response.status_code == 200, result[i])

from django.urls import reverse
from rest_framework.test import APITestCase

# Create your tests here.
from apps.user.models import APIUser


class APIUserTestCases(APITestCase):
    fixtures = [
        'apps/user/fixtures/data.json'
    ]

    def authenticate_user(self):
        """
        Authenticate user
        """
        token = APIUser.objects.filter(is_token_invalidated=False).first().token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_create_contact(self):
        self.authenticate_user()
        url = reverse('create_contact')
        response = self.client.post(
            url,
            {
                "uid": "test",
                "email": "",
                "first_name": "test",
                "last_name": "test",
                "phone": "test",
                "company": "test"
            },
            format='json'
        )
        self.contact_id = response.data.get('id')
        self.assertEqual(response.status_code, 201)

    def test_create_interest(self):
        self.test_create_contact()
        url = reverse('create_interest')
        response = self.client.post(
            url,
            {
                "contact": self.contact_id,
                'url': 'https://example.com',
                'category': 'Some category',
                'value': 'Some value'
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

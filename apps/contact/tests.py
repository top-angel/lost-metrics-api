from django.urls import reverse
from rest_framework.test import APITestCase

# Create your tests here.
from apps.user.models import APIUser


class ContactUserAPITest(APITestCase):
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
        url = reverse('contact-list')
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

    def test_list_contact(self):
        self.authenticate_user()
        url = reverse('contact-list')
        response = self.client.get(
            url,
        )
        self.assertEqual(response.status_code, 200)

    def test_update_contact(self):
        self.test_create_contact()
        url = reverse('contact-detail', args=[self.contact_id])
        response = self.client.patch(
            url,
            {
                "email": "test@gmail.com",
                "first_name": "test",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_contact(self):
        self.test_create_contact()
        url = reverse('contact-detail', args=[self.contact_id])
        response = self.client.get(
            url,
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_contact(self):
        self.test_create_contact()
        url = reverse('contact-detail', args=[self.contact_id])
        response = self.client.delete(
            url,
        )
        self.assertEqual(response.status_code, 204)


class InterestUserAPITest(APITestCase):
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
        url = reverse('contact-list')
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
        url = reverse('interest-list')
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
        self.interest_id = response.data.get('id')
        self.assertEqual(response.status_code, 201)

    def test_list_interest(self):
        self.authenticate_user()
        url = reverse('interest-list')
        response = self.client.get(
            url,
        )
        self.assertEqual(response.status_code, 200)

    def test_update_interest(self):
        self.test_create_interest()
        url = reverse('interest-detail', args=[self.interest_id])
        response = self.client.patch(
            url,
            {
                "email": "test@gmail.com",
                "first_name": "test",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_interest(self):
        self.test_create_interest()
        url = reverse('interest-detail', args=[self.interest_id])
        response = self.client.get(
            url,
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_interest(self):
        self.test_create_interest()
        url = reverse('interest-detail', args=[self.interest_id])
        response = self.client.delete(
            url,
        )
        self.assertEqual(response.status_code, 204)

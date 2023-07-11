from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

class MyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_oee_threshold_no_params(self):
        # Assuming you have dashproc objects with appropriate data in the database

        url = 'http://localhost:8000/api/oee/myendpoint/'

        # Make a GET request to the API view
        response = self.client.get(url)

        # Assertions for a successful response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertIn('data', response.data)


    def test_get_oee_threshold(self):
        # Create query parameters for the GET request
        params = {
            'machine': 'cam1',
            'start_date': '2023-02-22',
            'end_date': '2023-02-23',
        }

        url = 'http://localhost:8000/api/oee/myendpoint/'

        # Make a GET request to the API view with the query parameters
        response = self.client.get(url, params=params)

        # Assertions for the response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertIn('data', response.data)

        # Assertions for the response data
        thrhold_list = response.data['data']
        self.assertIsInstance(thrhold_list, list)

    def test_get_oee_threshold_error(self):

        url = 'http://localhost:8000/api/oee/myendpoint/'

        # Make a GET request that triggers an exception
        response = self.client.get(url)

        # Assertions for an error response
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('data', response.data)
        self.assertEqual(response.data['data'], "Failed to get the OEE threshold value")

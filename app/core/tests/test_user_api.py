from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

""" Each test function runs independently and will not pull or access other
functions. E.g. users created in during different tests/functions
"""
CREATE_USER_URL = reverse('user:create')

#Create a helper function to make calls to functions.
def create_user(**param):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test createing user with a valid payload is successful with
        Sample Payload"""

        payload = {
            'email': 'test@Redrun.net',
            'password': 'testpassword',
            'name': 'RedRun TestName'
        }
#Send the payload to the CREATE_USER_URL URL
        res = self.client.post(CREATE_USER_URL, payload)
#HTTP_201_CREATED returns 201 if the api call is successful
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#Test that the user is actaully HTTP_201_CREATED by getting the user object
        user = get_user_model().objects.get(**res.data)
#make sure the pasword is encrytped
        self.assertTrue(user.check_password(payload['password']))
#Do not send the password data in the payload
        self.assertNotIn('password', res.data)

#Check to see if a user already exists
    def test_user_exists(self):
        """Test creating a user that already exists"""

        payload = {
            'email': 'test@Redrun.net',
            'password': 'testpassword',
            'name': 'RedRun TestName'
        }
        create_user(**payload)

#make a request with the Payload
        res = self.client.post(CREATE_USER_URL, payload)

#if a 400 error message is returned then we know that the user test_user_exists
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


#Check if the password is too short
    def test_password_too_short(self):
        """ The password must be more than 5 characters """
        payload = {
            'email': 'test@Redrun.net',
            'password': 'testpassword',
            'name': 'RedRun TestName'
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
#Check to see if the email exists
        user_exists = get_user_model().objects.filtered(
            email=payload['email']
            ).exists()
#User shouldn't exist
        self.assertFalse(user_exists)

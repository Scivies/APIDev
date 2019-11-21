from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

""" Each test function runs independently and will not pull or access other
functions. E.g. users created in during different tests/functions
"""
CREATE_USER_URL = reverse('user:create')
#create user URL to test the token
TOKEN_URL = reverse('user:token')
#Create "ME" URL to test users can manage thier profiles
ME_URL = reverse('user:me')


#Create a helper function to make calls to functions.
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test createing user with a valid payload is successful with
        Sample Payload"""

        payload = {
            'email': 'test4@Redrun.net',
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
            'email': 'Test_User_Exists@Failededd.net',
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
            'email': 'test4@Redrun.net',
            'password': 'testpassword',
            'name': 'RedRun TestName'
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
#Check to see if the email exists
        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
#User shouldn't exist
        self.assertFalse(user_exists)

###############################################################
## CREATE TESTS FOR API CALLS FOR TOKENS
##############################################################

def test_create_token_for_user(self):
    """Test that a token is created for the user"""
    payload = {
        'email': 'test4@Redrunnnl.net',
        'password': 'testpassword',
        }
    create_user(**payload)
    res = self.client.post(TOKEN_URL, payload)
    #Test for the post response. KEY AND TOKEN SHOULD BE returned @ 200 message
    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

#Create test for invalid credentials are given
def test_create_token_invalid_credentials(self):
    """Test that token is not created if invalid credentials are given"""
    create_user(email='test4@Redrunnnl.net', password='testpassword')
    payload = {'email': 'test_token@redrun.net', 'password': 'wrong_password'}
    res = self.client.post()

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

def test_create_token_no_user(self):
    """Test that token is not created if the user doesn't exist"""
    payload = {'email': 'test_token@redrun.net', 'password': 'test_password'}
    res.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

def test_create_token_missing_field(self):
    """Test that email and password are required. We expect this to fail
    because no password/eamil is passed"""
    res = self.client.post(TOKEN_URL, { 'email': 'one', 'password': ''})

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, statu.HTTP_400_BAD_REQUEST)

######################################################################
##TEST THAT URL / USER TOKENS ARE AUTHORIZED
#####################################################################
def test_retrieve_user_unathorized(self):
    """Test that authication is required for users"""
    res = self.client.get(ME_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#Private indicates that tokens must be used.
class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
        email='test4@setUp.net',
        password='testpassword',
        name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    #Retrieve success of retrieving profile successfully
    def test_retrieve_profile_success(self):
        """Test retrieving profile for user logged in"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
        'name': self.user.name,
        'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

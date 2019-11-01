from django.test import TestCase
from django.contrib.auth import get_user_model

# Create user model
class ModelTests(TestCase):

#  """Test creating a new user with an email is successful"""
    def test_create_user_with_email_successful(self):
        email = 'test@redrun.com'
        password = 'Password123!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # Test to email for a new user is normalized
    def test_new_user_email_normalized(self):
            email = 'test@REDRUN.COM'
            user = get_user_model().objects.create_user(email, 'test123')

            self.assertEqual(user.email, email.lower())

    # Test that the email address is valid
    # The assert value error musst be created in the user model
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    ## Create a super user
    ## Super user model is a part of the djago PermissionsMixin function
    def test_create_new_super_user(self):
        user = get_user_model().objects.create_superuser(
            'test@redrun.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

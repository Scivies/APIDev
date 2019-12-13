from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

#Create sample user for testing with tags, ...etc
def sample_user(email='Testuser_11162019_1@redrun.net', password='password'):
    """Create Sample User"""
    return get_user_model().objects.create_user(email, password)



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

    #Create Tag model for app tags.
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
        user=sample_user(),
        name='Doing It Right'
        )

        self.assertEqual(str(tag), tag.name)

    #Test that the ingredient model exists and works
    def test_ingredient_str(self):
        """Test the ingredient string reprsentation"""
        Ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Potato'
        )

        self.assertEqual(str(Ingredient), Ingredient.name)

    def test_receipe_str(self):
        """Test the receipe string representation"""
        recipe = models.Recipe.objects.create(
        #add the required fields for the receipe to be tested
            user=sample_user(),
            title='Chicken and Dumplings',
            time_minutes=25,
            price=15.99

        )

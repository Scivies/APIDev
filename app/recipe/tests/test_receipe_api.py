from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer


#Create the URL for the test models
RECIPES_URL = reverse('recipe:recipe-list')
#recipe is the app and recipe-list is the list

#Helper function to test multiple recipes or tests against
#**params means that any addtional parameters will be passed
def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.99,
    }
    #python allows parameters to be overwritten
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

###################################################################

class PublicRecipeApiTest(TestCase):
    """Test unathenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

######################################################################

class PrivateRecipeApiTest(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
        'RecipeTest@redrun.net',
        'password'
                )
        self.client.force_authenticate(self.user)

    #Use our helper function to create reciepes
    def test_retrieve_recipes(self):
        """Test retrieving recipes for test user"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        #make the reqeust to the URl
        res = self.client.get(RECIPES_URL)

        #get the recipes for the user
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    #Test that the recipe is for the user
    def test_recipes_limited_to_user(self):
        """Test retrieving recipes that belong only to the user"""
        user2 = get_user_model().objects.create_user(
        'RecipeTest2@redrun.net',
        'password'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        #make the request to the URl
        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

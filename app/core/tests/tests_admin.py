# Admin page unit test
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


# create class for admin site

class AdminSiteTests(TestCase):

# need to create a setup function that will run our test
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin1@redrun.com',
            password='Password123!'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='admin@redrun.com',
            password='Password123!',
            name='Test user full name'
        )

    # Test to see if the users are in django admin
    # use the reverse function to call the admin page
    # using reverse will mean we do not have to update the url if it changes
    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    # Test that the change user page works
    #/admin/core/user/"id of user"/
    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

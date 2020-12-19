from rest_framework.test import APITestCase
from .models import CustomUser


class TestUserProfile(APITestCase):
    profile_url = '/user/profile'

    def setUp(self):
        # Authentication flow
        # # Creating a user that would be used for the authentication before the main testing preocess
        self.user = CustomUser.objects.create(
            username="dev_uc", password="uche1234")
        self.client.force_authenticate(user=self.user)

    def test_view_profile_all(self):
        response = self.client.get(self.profile_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(result) > 1)

    def test_view_profile_single(self):
        response = self.client.get(f"{self.profile_url/1}")
        print(response.json())

        # Asserting
        self.assertEqual(response.status_code, 200)

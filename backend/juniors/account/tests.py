from rest_framework.test import APITestCase
from user.models import CustomUser


class TestAuth(APITestCase):
    login_url = "/account/login"
    register_url = "/account/register"
    refresh_url = "/account/refresh"

    def test_register(self):
        payload = {
            "username": "uchetesting123",
            "password": "mypassword"
        }

        response = self.client.post(self.register_url, data=payload)

        # Testing to see if the response satus s created (201)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        # First creating and account
        payload = {
            "username": "uchetesting123",
            "password": "mypassword"
        }
        # To test login we need to register first
        self.client.post(self.register_url, data=payload)

        # now testing the login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        # Test if the staus code if 200
        self.assertEqual(response.status_code, 200)

        # Testing to know if there is a refresh and assess token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        # create account first
        payload = {
            "username": "uchetesting123",
            "password": "mypassword"
        }
        # To test register we need to login first
        self.client.post(self.register_url, data=payload)

        # now testing the login
        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()['refresh']

        # get refresh
        response = self.client.post(
            self.refresh_url, data={
                'refresh': refresh
            }
        )
        result = response.json()

        # Test if the staus code if 200
        self.assertEqual(response.status_code, 200)

        # Testing to know if there is a refresh and assess token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestRestPassword(APITestCase):
    pre_reset_url = "/account/pre-password-reset"
    reset_url = "/account/password-reset"
    login_url = "/account/login"

    def setUp(self):
        # Authentication flow
        # # Creating a user that would be used for the authentication before the main testing preocess
        self.user = CustomUser.objects.create(
            username="dev_uc", password="uche1234")
        self.client.force_authenticate(user=self.user)

    def test_pre_reset(self):
        # This is just a get result with out a payload but the user must be authenticataed first
        response = self.client.get(self.pre_reset_url)

        # assertion
        self.assertEqual(response.status_code, 200)

    def test_password_rest(self):
        # To reset password you have to be logined and you have to place in your url the encrypted link
        # Setup
        response = self.client.get(self.pre_reset_url)
        result = response.json()

        # Processing
        reset_url = result['reset-url']
        payload = {
            "password": "mynewpass"
        }
        # making the request
        response = self.client.post(
            f"{self.reset_url}/{reset_url}", data=payload)
        result = response.json()

        # Assertion
        self.assertTrue(result['success'])

        payload = {
            "username": "dev_uc",
            "password": "mynewpass"
        }

        response = self.client.post(self.login_url, data=payload)

        self.assertEqual(response.status_code, 200)

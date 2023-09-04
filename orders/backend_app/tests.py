from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from django.urls import reverse

from backend_app.models import User


class OrderTests(APITestCase):
    def test_order_history(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='aalex')
        response = factory.get(reverse('order_history'))
        force_authenticate(response, user=user, token=user.auth_token)
        print(response)


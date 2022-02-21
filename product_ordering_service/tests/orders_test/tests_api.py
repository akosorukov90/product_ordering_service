import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from orders.models import Contact


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='user1@local.com', password='g5U12gRny54`1235')
        self.assertEqual(user.email, 'user1@local.com')
        self.assertEqual(user.type, 'buyer')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="g5U12gRn432y5435")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('admin1@local.com', 'g5U12fdsgRny5435')
        self.assertEqual(admin_user.email, 'admin1@local.com')
        self.assertTrue(admin_user.is_active)
        self.assertEqual(admin_user.type, 'buyer')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin1@local.com', password='g5U12gcxvbRny5435', is_superuser=False)


@pytest.mark.django_db
def test_create_contact_user():
    data_user = {
                    'city': 'СПб',
                    'phone': '88123456789'
                }
    User = get_user_model()
    user2 = User.objects.create_user(email='user2@local.com', password='g5U12wewqgRny5435')
    client = APIClient()
    url = reverse('contacts_user-list')
    token1 = Token.objects.create(user=user2)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token1.key}')
    response = client.post(url, data=data_user)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_list_contact_admin_user(client):
    User = get_user_model()
    user3 = User.objects.create_user(email='user3@local.com', password='g5Unbvn12gRny5435')
    user4 = User.objects.create_user(email='user4@local.com', password='g5U12gjtyhRny5435')
    admin2 = User.objects.create_superuser(email='admin2@local.com', password='g5U12g3453erRny5435')
    contact1 = Contact.objects.create(user=user3, city='СПб', phone='88123456789')
    contact2 = Contact.objects.create(user=user4, city='МСК', phone='84953456789')

    client = APIClient()
    url = reverse('contacts_user-list')
    token2, created = Token.objects.get_or_create(user=admin2)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token2.key}')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_contact_simple_user(client):
    User = get_user_model()
    user5 = User.objects.create_user(email='user5@local.com', password='g5U12gRny5435')
    user6 = User.objects.create_user(email='user6@local.com', password='g5U12gRny5435')
    admin3 = User.objects.create_superuser(email='admin3@local.com', password='g5U12gRny5435')
    contact1 = Contact.objects.create(user=user5, city='СПб', phone='88123456789')
    contact2 = Contact.objects.create(user=user6, city='МСК', phone='84953456789')

    client = APIClient()
    url = reverse('contacts_user-list')
    token3, created = Token.objects.get_or_create(user=user5)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token3.key}')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

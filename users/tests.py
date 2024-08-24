from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Тестирует создание нового пользователя через API.
        """
        url = reverse('users:user_create')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'is_moderator': False,
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def get_jwt_token(self, user):
        """
        Возвращает JWT-токен для заданного пользователя.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'
        }

    def test_user_list(self):
        """
        Тестирует получение списка всех пользователей.
        Доступно только для аутентифицированных пользователей.
        """
        user = User.objects.create_user(
            email='user1@example.com',
            password='password123'
        )
        url = reverse('users:user_list')
        self.client.credentials(**self.get_jwt_token(user))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        """
        Тестирует получение данных о конкретном пользователе по его ID.
        Доступно только для аутентифицированных пользователей.
        """
        user = User.objects.create_user(
            email='user1@example.com',
            password='password123'
        )
        url = reverse('users:user_detail', kwargs={'pk': user.pk})
        self.client.credentials(**self.get_jwt_token(user))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user1@example.com')

    def test_user_update(self):
        """
        Тестирует обновление данных пользователя.
        Доступно только для аутентифицированных пользователей.
        """
        user = User.objects.create_user(
            email='user1@example.com',
            password='password123'
        )
        url = reverse('users:user_update', kwargs={'pk': user.pk})
        data = {'email': 'newemail@example.com', 'password': 'newpassword123'}
        self.client.credentials(**self.get_jwt_token(user))
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, 'newemail@example.com')

    # Тестирование удаления пользователя
    def test_user_delete(self):
        """
        Тестирует удаление пользователя.
        Доступно только для аутентифицированных пользователей.
        """
        user = User.objects.create_user(
            email='user1@example.com',
            password='password123'
        )
        url = reverse('users:user_delete', kwargs={'pk': user.pk})
        self.client.credentials(**self.get_jwt_token(user))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

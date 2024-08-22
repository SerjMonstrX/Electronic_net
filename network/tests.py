from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from network.models import NetworkEntity

User = get_user_model()


class NetworkEntityAPITests(TestCase):
    def setUp(self):
        """
        Устанавливаем начальные данные для тестов.
        Создаем пользователей, включая модератора, и несколько объектов сети.
        """
        self.client = APIClient()

        # Создаем пользователей
        self.user = User.objects.create_user(email='user@test.com', password='password123')
        self.moderator = User.objects.create_user(email='moderator@test.com', password='password123', is_moderator=True)
        self.other_user = User.objects.create_user(email='other@test.com', password='password123')

        # Создаем объекты сети
        self.factory = NetworkEntity.objects.create(
            creator=self.user,
            name='Завод',
            email='factory@test.com',
            country='Россия',
            supplier_type=0  # Завод
        )

        self.retail_network = NetworkEntity.objects.create(
            creator=self.user,
            name='Розничная сеть',
            email='retail@test.com',
            country='Россия',
            supplier=self.factory,
            supplier_type=1  # Розничная сеть
        )

        self.individual = NetworkEntity.objects.create(
            creator=self.other_user,
            name='ИП Иванов',
            email='individual@test.com',
            country='Россия',
            supplier=self.retail_network,
            supplier_type=2  # Индивидуальный предприниматель
        )

    def test_create_network_entity(self):
        """
        Тестирует создание нового объекта сети.
        Доступно только аутентифицированным пользователям.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Новая сеть',
            'email': 'new@test.com',
            'country': 'Россия',
            'supplier_type': 1,  # Розничная сеть
            'supplier': self.factory.id
        }

        response = self.client.post(reverse('network:networkentity-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkEntity.objects.count(), 4)
        self.assertEqual(response.data['name'], 'Новая сеть')

    def test_update_network_entity(self):
        """
        Тестирует обновление объекта сети.
        Разрешено только создателю или модератору.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Обновленная сеть',
            'email': 'updated@test.com',
            'country': 'Россия',  # Добавляем обязательное поле
            'supplier_type': 1,  # Также добавляем тип поставщика, если он обязателен
        }

        response = self.client.put(reverse('network:networkentity-update', args=[self.retail_network.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.retail_network.refresh_from_db()
        self.assertEqual(self.retail_network.name, 'Обновленная сеть')

    def test_moderator_can_update_any_entity(self):
        """
        Тестирует возможность модератора обновлять любой объект сети.
        """
        self.client.force_authenticate(user=self.moderator)

        data = {
            'name': 'Обновленная сеть модератором',
            'email': 'moderator-updated@test.com',
            'country': 'Россия',  # Добавляем обязательное поле
            'supplier_type': 2,  # Также добавляем тип поставщика, если он обязателен
        }

        response = self.client.put(reverse('network:networkentity-update', args=[self.individual.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.individual.refresh_from_db()
        self.assertEqual(self.individual.name, 'Обновленная сеть модератором')

    def test_non_creator_cannot_update(self):
        """
        Тестирует, что пользователь, не являющийся создателем, не может обновить объект сети.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Попытка обновления',
            'email': 'attempt@test.com'
        }

        response = self.client.put(reverse('network:networkentity-update', args=[self.individual.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_network_entity(self):
        """
        Тестирует удаление объекта сети.
        Доступно только создателю или модератору.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('network:networkentity-delete', args=[self.retail_network.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkEntity.objects.count(), 2)

    def test_non_creator_cannot_delete(self):
        """
        Тестирует, что пользователь, не являющийся создателем, не может удалить объект сети.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('network:networkentity-delete', args=[self.individual.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete_any_entity(self):
        """
        Тестирует возможность модератора удалять любой объект сети.
        """
        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(reverse('network:networkentity-delete', args=[self.individual.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkEntity.objects.count(), 2)

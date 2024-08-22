from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Product
from network.models import NetworkEntity

User = get_user_model()


class ProductAPITests(TestCase):
    def setUp(self):
        """
        Устанавливаем начальные данные для тестов:
        создаем пользователей, объект NetworkEntity и несколько продуктов.
        """
        self.client = APIClient()

        # Создаем пользователей
        self.user = User.objects.create_user(email='user@test.com', password='password123')
        self.moderator = User.objects.create_user(email='moderator@test.com', password='password123', is_moderator=True)
        self.other_user = User.objects.create_user(email='other@test.com', password='password123')

        # Создаем объект сети
        self.network_entity = NetworkEntity.objects.create(
            creator=self.user,
            name='Розничная сеть',
            email='retail@test.com',
            country='Россия',
            supplier_type=1
        )

        # Создаем продукты
        self.product1 = Product.objects.create(
            creator=self.user,
            network_entity=self.network_entity,
            name='Продукт 1',
            model='Модель 1',
            description='Описание продукта 1',
            release_date='2024-01-01'
        )

        self.product2 = Product.objects.create(
            creator=self.other_user,
            network_entity=self.network_entity,
            name='Продукт 2',
            model='Модель 2',
            description='Описание продукта 2',
            release_date='2024-02-01'
        )

    def test_create_product(self):
        """
        Тестирует создание нового продукта.
        Доступно только аутентифицированным пользователям.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Новый продукт',
            'model': 'Новая модель',
            'release_date': '2024-03-01',
            'network_entity': self.network_entity.id
        }

        response = self.client.post(reverse('products:product-create'), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(response.data['name'], 'Новый продукт')

    def test_update_product(self):
        """
        Тестирует обновление продукта.
        Разрешено только создателю или модератору.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Обновленный продукт',
            'model': 'Обновленная модель',
            'network_entity': self.network_entity.id
        }

        response = self.client.put(reverse('products:product-update', args=[self.product1.id]), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Обновленный продукт')

    def test_moderator_can_update_any_product(self):
        """
        Тестирует возможность модератора обновлять любой продукт.
        """
        self.client.force_authenticate(user=self.moderator)

        data = {
            'name': 'Обновленный продукт модератором',
            'model': 'Модель модератора',
            'network_entity': self.network_entity.id
        }

        response = self.client.put(reverse('products:product-update', args=[self.product2.id]), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product2.refresh_from_db()
        self.assertEqual(self.product2.name, 'Обновленный продукт модератором')

    def test_non_creator_cannot_update(self):
        """
        Тестирует, что пользователь, не являющийся создателем, не может обновить продукт.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Попытка обновления',
            'model': 'Несанкционированная модель'
        }

        response = self.client.put(reverse('products:product-update', args=[self.product2.id]), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        """
        Тестирует удаление продукта.
        Доступно только создателю или модератору.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('products:product-delete', args=[self.product1.id]))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_non_creator_cannot_delete(self):
        """
        Тестирует, что пользователь, не являющийся создателем, не может удалить продукт.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('products:product-delete', args=[self.product2.id]))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete_any_product(self):
        """
        Тестирует возможность модератора удалять любой продукт.
        """
        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(reverse('products:product-delete', args=[self.product2.id]))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

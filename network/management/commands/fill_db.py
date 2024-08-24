from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from network.models import NetworkEntity
from products.models import Product
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Очистить базу данных и заполнить тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write("Очистка базы данных...")

        # Очистка всех данных из моделей
        Product.objects.all().delete()
        NetworkEntity.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Создание пользователей...")

        # Создание пользователей
        users = [
            {'email': 'active1@example.com', 'is_active': True, 'is_moderator': False},
            {'email': 'active2@example.com', 'is_active': True, 'is_moderator': True},
            {'email': 'inactive1@example.com', 'is_active': False, 'is_moderator': False},
            {'email': 'inactive2@example.com', 'is_active': False, 'is_moderator': False},
        ]
        created_users = []
        for user_data in users:
            user = User.objects.create_user(
                email=user_data['email'],
                password='password123',
                is_active=user_data['is_active'],
                is_moderator=user_data['is_moderator']
            )
            created_users.append(user)

        # Создание суперпользователя
        User.objects.create_superuser(email='admin@admin.ru', password='1234')

        self.stdout.write("Создание объектов сети и продуктов...")

        # Создание объектов сети
        factory = NetworkEntity.objects.create(
            name='Завод 1',
            creator=created_users[0],
            email='factory1@f.ru',
            country='Россия',
            supplier_type=0,
        )

        retail_network = NetworkEntity.objects.create(
            name='Розничная сеть 1',
            creator=created_users[1],
            email='retail_net_1@f.ru',
            country='Россия',
            supplier=factory,
            supplier_type=1,
        )

        individual_entrepreneur = NetworkEntity.objects.create(
            name='ИП 1',
            creator=created_users[3],
            email='individual_ent_1@f.ru',
            country='Россия',
            supplier=retail_network,
            supplier_type=2,
        )

        NetworkEntity.objects.create(
            name='Розничная сеть 2',
            creator=created_users[2],
            email='retail_net_2@f.ru',
            country='Россия',
            supplier_type=1,
        )

        # Создание продуктов
        entities = NetworkEntity.objects.all()
        products = [
            Product(network_entity=entity, creator=created_users[i-1], name=f"Продукт {i+1}", model=f"Модель {i+1}",
                    release_date=date(2023, 1, i+1))
            for i, entity in enumerate(entities)
        ]
        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
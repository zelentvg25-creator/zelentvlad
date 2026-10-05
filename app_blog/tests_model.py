from django.test import TestCase
from .models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        # Создаем тестовую категорию специальным методом create()
        Category.objects.create(category='Тестова категорія', slug='test-category')

    def test_category_model(self):
        # Получаем созданный объект из тестовой БД
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), 'Тестова категорія')
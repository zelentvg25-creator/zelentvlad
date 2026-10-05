from django.test import TestCase
from django.urls import resolve, reverse
from .views import HomePageView


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)

    # ВОТ СЮДА ДОБАВЛЯЕТСЯ ТЕСТ ИЗ МЕТОДИЧКИ:
    def test_category_view_status_code(self):
        # Используем name из вашего urls.py ('article_category_list')
        # и передаем аргумент категории (например, 'it')
        url = reverse('article_category_list', args=('it',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
from datetime import datetime

from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from .context_processors import navigation_links
from .models import Article, ArticleImage
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


class ArticleNavigationTests(TestCase):
    def setUp(self):
        pub_date = timezone.make_aware(datetime(2026, 10, 5, 12))
        self.pandas_article = Article.objects.create(
            title='Основи роботи з Pandas для аналізу даних',
            slug='Pandas',
            pub_date=pub_date,
            body='Текст статті Pandas.',
        )
        self.navigation_articles = {'Pandas': self.pandas_article}
        for label, slug in (
            ('Python', 'Python'),
            ('NumPy', 'NumPy'),
            ('Machine Learning', 'Machine-Learning'),
        ):
            self.navigation_articles[label] = Article.objects.create(
                title=f'Стаття про {label}',
                slug=slug,
                pub_date=pub_date,
                body=f'Текст статті {label}.',
            )

    def test_pandas_navigation_opens_pandas_article(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, f'href="{self.pandas_article.get_absolute_url()}">Pandas</a>')

        article_response = self.client.get(self.pandas_article.get_absolute_url())
        self.assertEqual(article_response.status_code, 200)
        self.assertContains(article_response, self.pandas_article.title)
        self.assertContains(article_response, self.pandas_article.body)

    def test_navigation_links_open_matching_articles(self):
        links = navigation_links(None)['navigation_links']
        self.assertEqual(
            links,
            list(self.navigation_articles.items()),
        )

    def test_article_photos_appear_in_gallery_and_card(self):
        ArticleImage.objects.create(
            article=self.pandas_article,
            image='photos/pandas-1.jpg',
            title='Pandas фото 1',
        )
        ArticleImage.objects.create(
            article=self.pandas_article,
            image='photos/pandas-2.jpg',
            title='Pandas фото 2',
        )

        detail_response = self.client.get(self.pandas_article.get_absolute_url())
        self.assertContains(detail_response, '/media/photos/pandas-1.jpg')
        self.assertContains(detail_response, '/media/photos/pandas-2.jpg')
        self.assertContains(detail_response, 'Pandas фото 1')

        home_response = self.client.get(reverse('home'))
        self.assertContains(home_response, '/media/photos/pandas-1.jpg')
from django.contrib.staticfiles import finders
from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import TemplateView, DateDetailView, ListView
from .models import Article, Category


ARTICLE_COVER_FILES = {
    'AI': '4321.jpg',
    'Django': '321.png',
    'Pandas': '234.jpg',
    'Technology': '142.jpg',
    'first-post': '123.jpg',
    'Python': 'python-cover.svg',
    'NumPy': 'numpy-cover.svg',
    'Machine-Learning': 'machine-learning-cover.svg',
}


def assign_article_covers(articles):
    for article in articles:
        image_name = ARTICLE_COVER_FILES.get(article.slug)
        image_path = finders.find(f'image/{image_name}') if image_name else None
        if not image_path:
            raise ValueError(
                f'No unique cover image is configured for article "{article.title}". '
                'Add a unique cover file to static/image and map its slug in ARTICLE_COVER_FILES.'
            )
        article.cover_image_url = staticfiles_storage.url(f'image/{image_name}')
    return articles


class HomePageView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(
            main_page=True
        ).prefetch_related('images')
        context['articles'] = assign_article_covers(articles)
        return context


class ArticleDetail(DateDetailView):
    queryset = Article.objects.prefetch_related('images')
    date_field = 'pub_date'
    query_pk_and_slug = False
    month_format = '%m'
    allow_future = True
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assign_article_covers([self.object])
        images = self.object.images.all()
        if self.object.image:
            images = images.exclude(image=self.object.image.name)
        context['images'] = images
        return context


class ArticleList(ListView):
    model = Article
    template_name = 'articles_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return assign_article_covers(super().get_queryset().prefetch_related('images'))


class ArticleCategoryList(ArticleList):
    def get_queryset(self):
        articles = Article.objects.filter(
            category__slug=self.kwargs['slug']
        ).distinct().prefetch_related('images')
        return assign_article_covers(articles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(
            slug=self.kwargs['slug']
        ).first()
        return context
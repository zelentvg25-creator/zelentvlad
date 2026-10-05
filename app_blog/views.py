from django.shortcuts import render
from django.views.generic import TemplateView, DateDetailView, ListView
from .models import Article, Category


class HomePageView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(main_page=True)[:5]
        return context


class ArticleDetail(DateDetailView):
    model = Article
    date_field = 'pub_date'
    query_pk_and_slug = True
    month_format = '%m'
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['images'] = self.object.images.all()
        except AttributeError:
            context['images'] = None
        return context


class ArticleList(ListView):
    model = Article
    template_name = 'articles_list.html'
    context_object_name = 'items'


class ArticleCategoryList(ArticleList):
    def get_queryset(self):
        return Article.objects.filter(
            category__slug=self.kwargs['slug']
        ).distinct()
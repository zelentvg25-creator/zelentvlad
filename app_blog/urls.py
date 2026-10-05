# app_blog/urls.py
from django.urls import path
from app_blog import views

urlpatterns = [
    path(r'', views.HomePageView.as_view()),
]
from django.urls import path
from . import views

urlpatterns = [
# urls.py
    path('', views.HomePageView.as_view(), name='home'),
    path('articles/', views.ArticleList.as_view(), name='articles_list'),  # <-- ТУТ 'articles_list'
    path('articles/category/<slug:slug>/', views.ArticleCategoryList.as_view(), name='article_category_list'),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
path(r'articles/category/<slug>',
     views.ArticleCategoryList.as_view(),
     name='articles-category-list'),

]
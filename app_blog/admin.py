from django.contrib import admin

from .forms import ArticleImageForm
from .models import Article, ArticleImage, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}
    search_fields = ('category',)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    form = ArticleImageForm
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'slug', 'main_page')
    list_filter = ('main_page', 'category')
    search_fields = ('title', 'body', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ArticleImageInline,)
    fields = ('title', 'slug', 'body', 'pub_date', 'main_page', 'category', 'image')


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'filename')
    search_fields = ('title', 'article__title')

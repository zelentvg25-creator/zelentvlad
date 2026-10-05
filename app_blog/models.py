# -*- coding: utf-8 -*- 
from django.utils import timezone
from django.db import models
from django.urls import reverse


class Category(models.Model):
    category = models.CharField('Категорія', max_length=250, help_text='Максимум 250 сим.')
    slug = models.SlugField('Слаг', unique=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Категорія для публікації'
        verbose_name_plural = 'Категорії для публікацій'

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        try:
            url = reverse('articles-category-list', kwargs={'slug': self.slug})
        except:
            url = "/"
        return url


class Article(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    slug = models.SlugField('Слаг', unique=True, null=True, blank=True)
    body = models.TextField('Текст статті', blank=True)
    pub_date = models.DateTimeField('Дата публікації', default=timezone.now)

    main_page = models.BooleanField('Головна', default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категорія')
    image = models.ImageField('Зображення', upload_to='articles/', blank=True, null=True)

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        try:
            url = reverse('article_detail', kwargs={
                'year': self.pub_date.strftime("%Y"),
                'month': self.pub_date.strftime("%m"),
                'day': self.pub_date.strftime("%d"),
                'slug': self.slug,
            })
        except:
            url = "/"
        return url


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, verbose_name='Стаття', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Фото', upload_to='photos')
    title = models.CharField('Заголовок', max_length=250, help_text='Максимум 250 сим.', blank=True)

    class Meta:
        verbose_name = 'Фото для статті'
        verbose_name_plural = 'Фото для статті'

    def __str__(self):
        return self.title or f"Фото {self.id}"

    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1]
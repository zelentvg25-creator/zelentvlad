# -*- coding: utf-8 -*- 

from django.utils import timezone

from django.db import models
from django.urls import reverse


class Category(models.Model):
    category = models.CharField(u'Категорія',

                                max_length=250, help_text=u'Максимум 250 символів')
    slug = models.SlugField(u'Слаг')

    objects = models.Manager()

    class Meta:
        verbose_name = u'Категорія для публікації'
        verbose_name_plural = u'Категорії для публікацій'

    def __str__(self):
        return self.category


from django.db import models


class Article(models.Model):
    # Ваші існуючі поля...
    main_page = models.BooleanField('Головна', default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    # Додаємо поле для фото:
    image = models.ImageField('Зображення', upload_to='articles/', blank=True, null=True)

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

    def __str__(self):
        return f"Стаття №{self.id}"

    def get_absolute_url(self):
        try:
            url = reverse('news-detail',
                          kwargs={

                              'year': self.pub_date.strftime("%Y"),

                              'month': self.pub_date.strftime("%m"),

                              'day': self.pub_date.strftime("%d"),

                              'slug': self.slug,

                          })
        except:
            url = "/"
        return url


class ArticleImage(models.Model):
    article = models.ForeignKey(Article,

                                verbose_name=u'Стаття',
                                related_name='images',
                                on_delete=models.CASCADE)
    image = models.ImageField(u'Фото', upload_to='photos')
    title = models.CharField(u'Заголовок', max_length=250,
                             help_text=u'Максимум 250 сим.',

                             blank=True)

    class Meta:
        verbose_name = u'Фото для статті'
        verbose_name_plural = u'Фото для статті'

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1] 
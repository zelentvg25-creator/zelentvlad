from .models import Article


def navigation_links(request):
    article_slugs = ('Pandas', 'Python', 'NumPy', 'Machine-Learning')
    articles = {
        article.slug: article
        for article in Article.objects.filter(slug__in=article_slugs)
    }
    labels = (
        ('Pandas', 'Pandas'),
        ('Python', 'Python'),
        ('NumPy', 'NumPy'),
        ('Machine Learning', 'Machine-Learning'),
    )
    return {
        'navigation_links': [
            (label, articles[slug])
            for label, slug in labels
            if slug in articles
        ]
    }

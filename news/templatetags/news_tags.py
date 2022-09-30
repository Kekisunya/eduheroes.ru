from django import template
from django.db.models import Count, F

from news.models import NewsCategory

register = template.Library()


@register.inclusion_tag('news/categories_sidebar.html')
def categories_sidebar():
    categories = NewsCategory.objects.annotate(cnt=Count('category_news', filter=F('category_news__published'))).filter(cnt__gt=0)
    result = {
        'categories': categories
    }
    return result

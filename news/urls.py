from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsHome.as_view(), name='all_news'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='news_by_category'),
    path('post/<int:pk>', NewsDetailed.as_view(), name='news_detailed'),
    path('add/', login_required(NewsCreate.as_view(), login_url='login'), name='news_add'),
    path('post/<int:pk>/edit', NewsEdit.as_view(), name='news_edit'),
    path('my/', NewsByAuthor.as_view(), name='news_by_author'),
    path('post/<int:pk>/del', NewsDelete.as_view(), name='news_delete')
]
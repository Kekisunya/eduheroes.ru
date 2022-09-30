from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('search/', JobsList.as_view(), name='jobs_search'),
    path('<int:pk>/', JobCard.as_view(), name='job_detailed'),
    path('add/', login_required(JobCreate.as_view(), login_url='login'), name='job_add'),
    path('<int:pk>/edit', JobEdit.as_view(), name='job_edit'),
    path('my/', JobByUser.as_view(), name='jobs_by_user'),
    path('<int:pk>/del', JobDelete.as_view(), name='job_delete')
]
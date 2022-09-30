"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

# Views import
from user_login.views import *

urlpatterns = [
    path('', main_page, name='main'),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('jobs/', include('jobs.urls')),
    path('employees/', include('employees.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),
    path('my/crop_image/', crop_image, name='crop_image'),

    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset/', ResetPassword.as_view(), name='reset_pass'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('reset_confirm/<uidb64>/<token>/', NewPassword.as_view(), name='password_reset_confirm'),
    path('my/', change_credentials, name='my_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'published')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'updated_at', 'published')
    list_editable = ('published',)
    search_fields = ('title', 'content')
    form = NewsAdminForm


class NewsCategoryAdmin(admin.ModelAdmin):
    def category_news_count(self, obj):
        return obj.category_news.count()

    category_news_count.short_description = 'Количество статей'

    list_display = ('id', 'title', 'category_news_count')
    list_display_links = ('id', 'title')


admin.site.register(News, NewsAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(PostViews)

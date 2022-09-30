from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class News(models.Model):
    '''
    Класс постов в ленте
    '''
    title = models.CharField(
        max_length=150,
        verbose_name='Заголовок',
        help_text='Заголовок поста, до 150 символов'
    )
    abstract = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Реферат',
        help_text='Небольшое превью к новости, максимум 300 символов'
    )
    image = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        blank=True,
        verbose_name='Изображение',
        help_text='Картинка для отображения рядом с новостью'
    )
    content = RichTextUploadingField(
        verbose_name='Текст',
        help_text='Текст поста в разметке HTML'
    )
    attached_files = models.FileField(
        upload_to='files/%Y/%m/%d/',
        blank=True,
        verbose_name='Прикрепленные файлы',
        help_text='Прикрепленные к новости файлы'
    )
    created_at = models.DateField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата создания'
    )
    updated_at = models.DateField(
        auto_now=True,
        editable=False,
        verbose_name='Дата обновления'
    )
    categories = models.ManyToManyField(
        'NewsCategory',
        verbose_name='Категории',
        blank=True,
        help_text='Категории поста',
        related_name='category_news',
    )
    authors = models.ManyToManyField(
        User,
        verbose_name='Авторы',
        related_name='author_news',
    )
    published = models.BooleanField(
        default=False,
        verbose_name='Опубликована'
    )
    views = models.ManyToManyField(
        'PostViews',
        verbose_name='Просмотры',
        blank=True,
        related_name='view_news',
        editable=False,
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at', '-pk']

    def __str__(self):
        s = 'Название {0}\nРеферат {1}\n Авторы {2}'.format(self.title, self. abstract, self.authors)
        return s

    def get_absolute_url(self):
        return reverse_lazy('news_detailed', kwargs={'pk': self.pk})

    def get_absolute_edit_url(self):
        return reverse_lazy('news_edit', kwargs={'pk': self.pk})

    def total_views(self):
        return self.views.count()


class NewsCategory(models.Model):
    '''
    Класс категорий постов в ленте
    '''
    title = models.CharField(max_length=50, verbose_name='Название категории', blank=False,
                             help_text='Название категории, до 50 символов')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('news_by_category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория статей'
        verbose_name_plural = 'Категории статей'


class PostViews(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Просмотр статьи'
        verbose_name_plural = 'Просмотры статей'


from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from math import sin, cos, acos, pi

User = get_user_model()


class Job(models.Model):
    '''
    Класс анкет работ
    '''
    title = models.CharField(
        verbose_name='Название вакансии',
        max_length=150
    )
    contacts = models.CharField(
        verbose_name='Контакты',
        max_length=150
    )
    description = RichTextUploadingField(
        verbose_name='Описание вакансии',
    )
    job_types = models.ManyToManyField(
        'JobType',
        verbose_name='Типы зантости',
        blank=True,
        related_name='jobtype_jobs'
    )
    remote = models.ManyToManyField(
        'JobRemote',
        verbose_name='Тип работы',
        blank=True,
        related_name='jobremote_jobs'
    )
    role = models.ForeignKey(
        'employees.EmployeeRole',
        verbose_name='Роль',
        on_delete=models.PROTECT,
        blank=True,
        related_name='employeerole_jobs'
    )
    students = models.ForeignKey(
        'JobStudents',
        verbose_name='Ученики',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='jobstudents_jobs'
    )
    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
        editable=False,
    )
    views = models.ManyToManyField(
        'JobViews',
        verbose_name='Просмотры',
        blank=True,
        related_name='view_jobs',
        editable=False,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        default=True,
        related_name='user_jobs'
    )
    location = models.CharField(
        verbose_name='Город',
        max_length=200,
        blank=True,
    )
    location_id = models.TextField(
        verbose_name='ID города',
        blank=True,
    )
    longitude = models.FloatField(
        verbose_name='Широта',
        blank=True,
        null=True
    )
    latitude = models.FloatField(
        verbose_name='Долгота',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at', '-pk']

    def __str__(self):
        s = 'ID: {0}\nНазвание: {1}\nКонтакты: {2}'.format(self.user, self.title, self.contacts)
        return s

    def get_username(self):
        return User.objects.get(pk=self.user.pk).username

    def get_absolute_url(self):
        return reverse_lazy('job_detailed', kwargs={'pk': self.pk})

    def get_absolute_edit_url(self):
        return reverse_lazy('job_edit', kwargs={'pk': self.pk})

    def total_views(self):
        return self.views.count()

    def get_distance(self, latitude, longitude):
        if self.longitude is None or self.latitude is None:
            return None
        r = 6371.21
        phi1 = self.latitude * pi / 180
        phi2 = latitude * pi / 180
        lambda1 = self.longitude * pi / 180
        lambda2 = longitude * pi / 180
        d = acos(
            sin(phi1) * sin(phi2) + \
            cos(phi1) * cos(phi2) * \
            cos(lambda1 - lambda2)
        )
        l = d * r
        return l


class JobType(models.Model):
    '''
    Типы работ, хотелки
    '''
    title = models.CharField(
        verbose_name='Название типа занятости',
        max_length=150)

    class Meta:
        verbose_name = 'Тип занятости'
        verbose_name_plural = 'Типы занятости'
        ordering = ['title',]

    def __str__(self):
        return self.title


class JobRemote(models.Model):
    '''
    Типы работ, хотелки
    '''
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип работы'
        verbose_name_plural = 'Типы работы'
        ordering = ['title',]


class JobViews(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Просмотр вакансии'
        verbose_name_plural = 'Просмотры вакансий'


class JobStudents(models.Model):
    '''
    Категории учеников
    '''
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория учеников'
        verbose_name_plural = 'Категории учеников'
        ordering = ['title',]

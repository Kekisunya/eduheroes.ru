from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from math import sin, cos, acos, pi

User = get_user_model()


def user_resume_path(instance, filename):
    '''
    file will be uploaded to MEDIA_ROOT/user_<id>/resumes
    :param instance:
    :return: string
    '''
    return 'user_files/user_{0}/resumes/{1}'.format(instance.user.id, filename)


class Employee(models.Model):
    '''
    Класс анкет соискателей
    '''
    resume = RichTextUploadingField(
        verbose_name='О себе',
        help_text='Текст о себе в разметке HTML'
    )
    resume_file = models.FileField(
        verbose_name='Файл с резюме',
        upload_to=user_resume_path,
        blank=True,
        help_text='Файл с резюме'
    )
    portfolio = models.TextField(
        verbose_name='Ссылки на работы',
        blank=True
    )
    job_types = models.ManyToManyField(
        'jobs.JobType',
        verbose_name='Тип занятости',
        blank=True,
        related_name='jobtype_employees'
    )
    rating = models.DecimalField(
        verbose_name='Рейтинг',
        max_digits=3,
        decimal_places=2,
        editable=False,
        default=0
    )
    times_rated = models.SmallIntegerField(
        verbose_name='Кол-во оценок',
        default=0,
        editable=False)
    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
        editable=False
    )
    approved = models.BooleanField(
        verbose_name='Опубликовано',
        default=False
    )
    views = models.ManyToManyField(
        'EmployeeViews',
        verbose_name='Просмотры',
        blank=True,
        related_name='view_employees',
        editable=False,
    )
    contacts = models.CharField(
        verbose_name='Контакты',
        max_length=150,
    )
    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        default=True
    )
    roles = models.ManyToManyField(
        'EmployeeRole',
        verbose_name='Роли',
        blank=True,
        related_name='role_employees'
    )
    students = models.ManyToManyField(
        'jobs.JobStudents',
        verbose_name='Ученики',
        blank=True,
        related_name='jobstudents_employees'
    )
    remote = models.ManyToManyField(
        'jobs.JobRemote',
        verbose_name='Тип работы',
        blank=True,
        related_name='jobremote_employees'
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
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'
        ordering = ['-created_at', '-pk']

    def __str__(self):
        s = 'ID: {0}\nКонтакты: {1}'.format(self.user, self.contacts)
        return s

    def get_username(self):
        return User.objects.get(pk=self.user.pk).username

    def get_absolute_url(self):
        return reverse_lazy('employee_detailed', kwargs={'pk': self.pk})

    def total_views(self):
        return self.views.count()

    def get_distance(self, latitude, longitude):
        if self.longitude is None or self.latitude is None:
            return None
        r = 6371.21
        phi1 = self.latitude * pi /180
        phi2 = latitude * pi /180
        lambda1 = self.longitude * pi /180
        lambda2 = longitude * pi /180
        d = acos(
            sin(phi1) * sin(phi2) + \
            cos(phi1) * cos(phi2) * \
            cos(lambda1 - lambda2)
        )
        l = d * r
        return l



class EmployeeRole(models.Model):
    title = models.CharField(
        verbose_name='Название роли',
        max_length=150
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title


class EmployeeViews(models.Model):
    ip = models.GenericIPAddressField()

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.ip

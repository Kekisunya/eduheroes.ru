# Generated by Django 4.1.1 on 2022-09-22 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='job_types',
            field=models.ManyToManyField(blank=True, related_name='jobtype_employees', to='jobs.jobtype', verbose_name='Тип занятости'),
        ),
        migrations.AddField(
            model_name='employee',
            name='remote',
            field=models.ManyToManyField(blank=True, related_name='jobremote_employees', to='jobs.jobremote', verbose_name='Тип работы'),
        ),
        migrations.AddField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='role_employees', to='employees.employeerole', verbose_name='Роли'),
        ),
        migrations.AddField(
            model_name='employee',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='jobstudents_employees', to='jobs.jobstudents', verbose_name='Ученики'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='employee',
            name='views',
            field=models.ManyToManyField(blank=True, editable=False, related_name='view_employees', to='employees.employeeviews', verbose_name='Просмотры'),
        ),
    ]

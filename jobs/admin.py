from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import *


class JobAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Job
        fields = '__all__'


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_views',  'location', 'created_at', 'updated_at',)
    list_display_links = ('id', 'user')
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('user',)
    form = JobAdminForm


class JobTypeAdmin(admin.ModelAdmin):
    def jobtype_jobs_count(self, obj):
        return obj.jobtype_jobs.count()

    def jobtype_employees_count(self, obj):
        return obj.jobtype_employees.count()

    jobtype_jobs_count.short_description = 'Количество вакансий'
    jobtype_employees_count.short_description = 'Количество соискателей'

    list_display = ('id', 'title', 'jobtype_jobs_count', 'jobtype_employees_count')
    list_display_links = ('id', 'title')


class JobRemoteAdmin(admin.ModelAdmin):
    def jobremote_jobs_count(self, obj):
        return obj.jobremote_jobs.count()

    def jobremote_employees_count(self, obj):
        return obj.jobtype_employees.count()

    jobremote_jobs_count.short_description = 'Количество вакансий'
    jobremote_employees_count.short_description = 'Количество соискателей'

    list_display = ('id', 'title', 'jobremote_jobs_count')
    list_display_links = ('id', 'title')


class JobStudentsAdmin(admin.ModelAdmin):
    def jobstudents_jobs_count(self, obj):
        return obj.jobstudents_jobs.count()

    def jobstudents_employees_count(self, obj):
        return obj.jobstudents_employees.count()

    jobstudents_jobs_count.short_description = 'Количество вакансий'
    jobstudents_employees_count.short_description = 'Количество соискателей'

    list_display = ('id', 'title', 'jobstudents_jobs_count', 'jobstudents_employees_count')
    list_display_links = ('id', 'title')


admin.site.register(Job, JobAdmin)
admin.site.register(JobType, JobTypeAdmin)
admin.site.register(JobViews)
admin.site.register(JobRemote, JobRemoteAdmin)
admin.site.register(JobStudents, JobStudentsAdmin)

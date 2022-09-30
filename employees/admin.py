from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import *


class EmployeeAdminForm(forms.ModelForm):
    resume = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'total_views', 'location', 'created_at', 'updated_at', 'approved')
    list_display_links = ('id', 'user')
    list_filter = ('created_at', 'updated_at', 'approved', 'rating')
    list_editable = ('approved',)
    search_fields = ('user',)
    form = EmployeeAdminForm


class EmployeeRoleAdmin(admin.ModelAdmin):
    def role_employees_count(self, obj):
        return obj.role_employees.count()

    role_employees_count.short_description = 'Количество соискателей'

    list_display = ('id', 'title', 'role_employees_count')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeRole, EmployeeRoleAdmin)
admin.site.register(EmployeeViews)

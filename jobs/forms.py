from captcha.fields import CaptchaField, CaptchaTextInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth import get_user_model

from employees.models import EmployeeRole
from .models import Job, JobType, JobRemote, JobStudents

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class JobsSearchForm(forms.Form):
    created_after = forms.DateField(
        label='Дата обновления',
        required=False,
        input_formats='%d.%m.%y',
        widget=DateInput(attrs={
            'class': 'form-control'
        }))
    employers = User.objects.filter(
        pk__in=Job.objects.values('user').all().distinct()
    )
    created_by = forms.ModelMultipleChoiceField(
        label='Автор',
        queryset=employers,
        required= False,
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    job_types = forms.ModelMultipleChoiceField(
        label='Тип занятости',
        queryset=JobType.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    roles = forms.ModelMultipleChoiceField(
        label='Роль',
        queryset=EmployeeRole.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    remote = forms.ModelMultipleChoiceField(
        label='Тип работы',
        queryset=JobRemote.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    students = forms.ModelMultipleChoiceField(
        label='Тип обучения',
        queryset=JobStudents.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    location = forms.CharField(
        label='Местоположение',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'location'
        })
    )
    location_id = forms.CharField(
        max_length=300,
        required=False,
        label='ID города',
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'id': 'location_id'
        })
    )
    longitude = forms.CharField(
        max_length=300,
        required=False,
        label='ID города',
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'id': 'longitude'
        })
    )
    latitude = forms.CharField(
        max_length=300,
        required=False,
        label='ID города',
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'id': 'latitude'
        })
    )
    radius = forms.IntegerField(
        label='Радус поиска',
        max_value=40000,
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
    )


class JobCreateForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget
    )
    captcha = CaptchaField(
        widget=CaptchaTextInput
    )

    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'role',
            'job_types',
            'students',
            'remote',
            'contacts',
            'location',
            'location_id',
            'longitude',
            'latitude',
            'captcha'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'contacts': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'location'
            }),
            'location_id': forms.HiddenInput(attrs={
                'class': 'form-control',
                'id': 'location_id'
            }),
            'longitude': forms.HiddenInput(attrs={
                'class': 'form-control',
                'id': 'longitude'
            }),
            'latitude': forms.HiddenInput(attrs={
                'class': 'form-control',
                'id': 'latitude'
            }),
            'job_types': forms.SelectMultiple(attrs={
                'class': 'custom-select'
            }),
            'remote': forms.SelectMultiple(attrs={
                'class': 'custom-select'
            }),
            'role': forms.Select(attrs={
                'class': 'custom-select'
            }),
            'students': forms.Select(attrs={
                'class': 'custom-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empty_label = None
        self.fields['students'].empty_label = None

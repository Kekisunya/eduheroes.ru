from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Employee, EmployeeRole
from jobs.models import JobType, JobStudents, JobRemote


class EmployeeSearchForm(forms.Form):
    job_types = forms.ModelMultipleChoiceField(
        queryset=JobType.objects.all(),
        required=False,
        label='Интересы',
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    min_rating = forms.DecimalField(
        max_value=10,
        min_value=0,
        max_digits=3,
        decimal_places=2,
        required=False,
        label='Минимальный рейтинг',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    max_rating = forms.DecimalField(
        max_value=10,
        min_value=0,
        max_digits=3,
        decimal_places=2,
        required=False,
        label='Максимальный рейтинг',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }))
    roles = forms.ModelMultipleChoiceField(
        queryset=EmployeeRole.objects.all(),
        required=False,
        label='Роль',
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    students = forms.ModelMultipleChoiceField(
        queryset=JobStudents.objects.all(),
        required=False,
        label='Тип обучения',
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    remote = forms.ModelMultipleChoiceField(
        queryset=JobRemote.objects.all(),
        required=False,
        label='Тип работы',
        widget=forms.SelectMultiple(attrs={
            'class': 'custom-select'
        })
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        label='Город',
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
        max_value=40000,
        min_value=0,
        required=False,
        label='Радиус',
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
    )


class EmployeeCreateForm(forms.ModelForm):
    resume = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Employee
        fields = [
            'resume',
            'resume_file',
            'portfolio',
            'job_types',
            'contacts',
            'roles',
            'remote',
            'students',
            'location',
            'location_id',
            'longitude',
            'latitude'
        ]
        widgets = {
            'portfolio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
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
            'roles': forms.SelectMultiple(attrs={
                'class': 'custom-select'
            }),
            'students': forms.SelectMultiple(attrs={
                'class': 'custom-select'
            }),
        }

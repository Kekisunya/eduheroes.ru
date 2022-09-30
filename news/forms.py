from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth import get_user_model

from .models import News

User = get_user_model()


class NewsCreateForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    captcha = CaptchaField(widget=CaptchaTextInput)

    class Meta:
        model = News
        fields = ['title', 'abstract', 'image', 'attached_files', 'content', 'categories', 'authors', 'captcha']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'custom-select',
            }),
            'authors': forms.SelectMultiple(attrs={
                'class': 'custom-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super_kwargs = kwargs.copy()
        user = super_kwargs.pop('user')
        super().__init__(*args, **super_kwargs)
        self.fields['authors'].queryset = User.objects.exclude(pk=user.id)

    def save(self, commit=True):
        author = User.objects.all().difference(self.fields['authors'].queryset)
        self.cleaned_data['authors'] = self.cleaned_data['authors'].union(author)
        return super().save()



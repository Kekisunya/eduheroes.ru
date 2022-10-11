from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django import forms

from captcha.fields import CaptchaField, CaptchaTextInput

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'on'
        })
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'on'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    captcha = CaptchaField(widget=CaptchaTextInput)

    class Meta:
        model = User
        fields = ("email", "username", 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'on'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'on'
        })
    )
    captcha = CaptchaField(widget=CaptchaTextInput)


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'id': 'id_input_email',
            'placeholder': 'Введите email',
        })
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_input_username',
            'placeholder': 'Введите имя пользователя',
        })
    )
    userpic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'd-none',
            'id': 'id_profile_image_file_selector',
            'name': 'profile_image_file_selector',
            'onchange': 'readURL(this)'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'userpic')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.exclude(email=self.initial['email']).get(email=email)
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(username=self.initial['username']).get(username=username)
        except User.DoesNotExist:
            return username

    def save(self, request, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        if self.cleaned_data['username'] != self.initial['username']:
            user.username = self.cleaned_data['username']
        if self.cleaned_data['email'] != self.initial['email']:
            user.email = self.cleaned_data['email']
        if self.cleaned_data['userpic'] != self.initial['userpic']:
            user.userpic = self.cleaned_data['userpic']
        if commit:
            user.save()
        return user



class ChangePassForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'old_password',
            'id': 'id_old_password',
            'placeholder': 'Введите текущий пароль',
            'autocomplete': 'on',
        })
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'new_password1',
            'id': 'id_new_password1',
            'placeholder': 'Новый пароль',
            'autocomplete': 'on',
        })
    )
    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'new_password2',
            'id': 'id_new_password2',
            'placeholder': 'Повторите новый пароль',
            'autocomplete': 'on',
        })
    )
    class Meta:
        model = User

class ResetPassForm(SetPasswordForm):
    captcha = CaptchaField(widget=CaptchaTextInput)
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
            login(request, self.user)
        return self.user
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        if not username:
            raise ValueError('Пользователь должен иметь имя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_userpic_path(self, filename):
    return 'user_files/user_{0}/photos/{1}'.format(self.pk, filename)


def get_default_userpic():
    return 'default_userpic/default_userpic.png'


class MyUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='Email',
        max_length=60,
        unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=30,
        unique=True
    )
    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='Последнее посещение',
        auto_now=True
    )
    is_admin = models.BooleanField(
        verbose_name='Админ',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True
    )
    is_superuser = models.BooleanField(
        verbose_name='Суперюзер',
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name='Персонал',
        default=False
    )
    userpic = models.ImageField(
        verbose_name='Картинка профиля',
        upload_to=get_userpic_path,
        default=get_default_userpic
    )
    hide_email = models.BooleanField(
        verbose_name='Спрятать email',
        default=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label = 'auth'

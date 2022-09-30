from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def has_no_employee(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, edit_url=None
):
    """
    Декоратор проверяет, есть ли у юзера анкета, и, если есть,
    перенаправляет его со страницы создания на страницу редакции
    """
    def func(user):
        try:
            user.employee
            return False
        except:
            return True

    actual_decorator = user_passes_test(
        func,
        login_url=edit_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

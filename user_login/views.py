import base64
import json
import os

import cv2
import numpy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core import files
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from mysite import settings
from .forms import UserCreateForm, UserLoginForm, ChangePassForm, UserEditForm
from .tokens import account_activation_token

TEMP_PROFILE_IMAGE_NAME = 'temp_profile_image.png'
INCORRECT_PADDING_EXCEPTION = 'Incorrect padding'
User = get_user_model()


def main_page(request):
    context = {
        'header': True,
        'title': 'Главная'
    }
    return render(request, 'main.html', context)


def activate_email(request, user, to_email):
    mail_subject = 'Активация аккаунта на EDU Heroes'
    message = render_to_string('user_login/template_activate_account.html',{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'

    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'<b>{user}</b>, мы отапвили тебе на почту <b>{to_email}</b> письмо с ссылкой для активации профиля. \n Перейди по ней, чтобы завершить регистрацию.')
    else:
        messages.success(request, f'Проблема с отправкой письма с кодом подтверждения')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(user)
    print(account_activation_token.check_token(user, token))

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Регистрация успешно завершена!')
        return redirect('main')
    else:
        messages.error(request, 'Недействительная ссылка для активации аккаунта')
    return redirect('main')


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('main')
        else:
            messages.error(request, 'Ошибка')
    form = UserCreateForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'user_login/signup.html', context)


def user_login(request):
    redirect_to = request.GET.get('next', '/')
    redirect_to = redirect_to if redirect_to != '/login/' else '/'
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
    else:
        form = UserLoginForm()
    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'user_login/login.html', context)


def user_logout(request):
    redirect_to = 'login'
    logout(request)
    return redirect(redirect_to)


class ResetPassword(PasswordResetView):
    success_url = '/'
    template_name = 'user_login/password_reset.html'


class NewPassword(PasswordResetConfirmView):
    success_url = '/login/'
    template_name = 'user_login/password_reset_complete.html'


def save_temp_profile_image_from_base64string(image_string, user):
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(f'{settings.TEMP}\\{str(user.pk)}'):
            os.mkdir(f'{settings.TEMP}\\{str(user.pk)}')
        url = os.path.join(f'{settings.TEMP}\\{str(user.pk)}', TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(image_string)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            image_string += "=" * ((4 - len(image_string) % 4) % 4)
            return save_temp_profile_image_from_base64string(image_string, user)
    return None


def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            image_string = request.POST.get('image')
            url = save_temp_profile_image_from_base64string(image_string, user)
            stream = open(url, "rb")
            bts = bytearray(stream.read())
            np_array = numpy.asarray(bts, dtype=numpy.uint8)
            img = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
            stream.close()

            crop_x = int(float(str(request.POST.get('cropX'))))
            crop_y = int(float(str(request.POST.get('cropY'))))
            crop_width = int(float(str(request.POST.get('cropWidth'))))
            crop_height = int(float(str(request.POST.get('cropHeight'))))

            if crop_x < 0:
                crop_x = 0
            if crop_y < 0:
                crop_y = 0
            crop_img = img[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

            is_success, im_buf_arr = cv2.imencode('.png', crop_img)
            im_buf_arr.tofile(url)

            if user.userpic.url[-5].isdigit():
                n_loc = -5
                while user.userpic.url[n_loc - 1].isdigit():
                    n_loc -= 1
                n = int(user.userpic.url[n_loc:-4])
            else:
                n = -1
            user.userpic.delete()
            f = files.File(open(url, 'rb'))
            user.userpic.save('profile_image_'+str(n+1)+'.png', f)
            f.close()
            user.save()

            payload['result'] = 'success'
            payload['cropped_profile_image'] = user.userpic.url

            os.remove(url)

        except Exception as e:
            payload['result'] = 'error'
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type='application/json')


@login_required(login_url='login')
def change_credentials(request):
    user = request.user
    if request.method == "POST":
        if request.POST.get('button') == 'password':
            pass_form = ChangePassForm(data=request.POST, user=user)
            if pass_form.is_valid():
                pass_form.save()
                update_session_auth_hash(request, pass_form.user)
                return redirect('my_profile')
        else:
            user_form = UserEditForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                return redirect('my_profile')
    user_form = UserEditForm(initial = {
        'email': user.email,
        'username': user.username,
    })
    context = {
        'user_form': user_form,
        'pass_form': ChangePassForm(user),
        'Title': 'Учетные данные'
    }
    return render(request, 'user_login/my_profile.html', context)

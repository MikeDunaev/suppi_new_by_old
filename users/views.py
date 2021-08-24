from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, AddShopForm, ContactForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Seller
from users.services.process_profile_data import process_data_from_profile
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.views import View
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text


def pay(request):
    return render(request, 'users/pay.html')


def after_register(request):
    return render(request, 'users/after_register.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            if form.is_valid():
                email_to = form.cleaned_data.get('email')
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(
                    'Активация аккаунта',
                    message,
                    'info@suppi.ru',
                    [email_to],
                )
                email.send(fail_silently=False)
                Seller.objects.create(user_id=user.id, current_shop=0)
                messages.success(request, 'Успешная регистрация!')
                return redirect('after_register')
            else:
                messages.error(request, 'Ошибка при регистрации')
        else:
            messages.error(request, 'Пользователь с таким email уже существует!')
    else:
        form = UserRegisterForm()
        messages.error(request, 'Ошибка при отправки формы')
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Account activated successfully')
    return redirect('profile')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})



@login_required
def profile(request):
    try:
        form, shops = process_data_from_profile(request=request)
    except Exception as ex:
        messages.error(request, 'Ошибка получения данных пользователя')
        logger.error(ex)
        form = AddShopForm()
        shops = []
    user = request.user
    current_shop = Seller.objects.get(user_id=user).current_shop

    return render(request, 'users/profile.html', {'form': form, 'shops': shops, 'current_shop': current_shop})
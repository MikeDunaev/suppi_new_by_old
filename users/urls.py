from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('activate/<uidb64>/<token>',
            activate, name='activate'),
    path('please-activate', after_register, name='after_register'),
    path('pay', pay, name='pay'),
	path('contact/', send_mail, name='contact'),
    # path('activate/<uidb64>/<token>',
    #          Verification.as_view(), name='activate'),
]
from django.urls import path
from . import views



from django.urls import path

from .views import (
    LogInView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView,
    ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView,
)

app_name = 'user'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    #path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),







    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('newsletter/', views.register_form, name='register_form'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.sign_up, name='signup'),
    path('reg', views.reg, name='reg'),
    path('user', views.user, name='user'),
    path('login', views.loginuser, name='loginuser'),
    path('test', views.test, name='test'),
    #path('loginpage/', views.loginpage, name='loginpage'),
    
    path('index/', views.index, name='index'),
    path('welcome/', views.register, name='register'),
    path("awelcome/", views.awelcome, name="awelcome"),
    path("takeme/", views.takeme, name="takeme"),
    
    
]

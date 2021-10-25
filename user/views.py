
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import newsletter_form, CreateUserForm, join_form
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required



from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
     LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
     PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
 )
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings

from .utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
 )
from .forms import (
    SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
    RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
    ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeProfileForm, ChangeEmailForm,
 )
from .models import Activation


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'user/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)


        return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpView(GuestOnlyView, FormView):
    template_name = 'user/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            # Set a temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        # Create a user record
        user.save()

        # Change the username to the "user_ID" form
        if settings.DISABLE_USERNAME:
            user.username = f'user_{user.id}'
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, _('To activate your account, follow the link sent to your  email.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('You are successfully signed up!'))

        return redirect('/welcome')


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('user:log_in')


class ResendActivationCodeView(GuestOnlyView, FormView):
    template_name = 'user/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('user:resend_activation_code')


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'user/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('user:restore_password_done')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'user/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('user:change_profile')


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'user/profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('user:change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('user:change_email')


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'user/remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('user:remind_username')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'user/profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()
        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('user:change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'user/restore_password_confirm.html'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('user:log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'user/restore_password_done.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'user/log_out.html'


def index(request):
    return render (request, 'user/index.html')
def test(request):
    form = CreateUserForm()
    context = {'form':form}
    return render (request, 'user/create.html', context)
def user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse('You have successfully sign up for our news letter')
        

    #Registration form view
def register_form(request):
    form = newsletter_form()
    context = {'form':form}
    if request.method == 'POST':
        form = newsletter_form(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse('You have successfully sign up for our news letter')
    return render (request, 'user/register.html',  context)
    

def sign_up(request):
    form = join_form(request.POST)
    context = {'form':form}
    return render(request, 'user/sign_up.html',context)
def reg(request):
    if request.method == 'POST':
        form = join_form(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already Exists')
                return redirect('/sign_up')

            else:
                user = form.save(commit=False)
            user.password = make_password('user.password')
            user.save()
            newuser = form.cleaned_data.get('first_name')
            messages.success(request, 'Success! welcome' + newuser + ' ' + ', You have successfully registered.')
            return redirect('/register')
        

def register(request):
    first_name = request.POST.get('first_name')
    context = {
        'first_name': first_name,
        'achievement': 'registered'
    }
    user = request.user.pk
    return render(request, 'user/success.html', context, user)

def home(request):
    return render (request, 'user/index1.html')
    #return HttpResponse ('All assets are recoverable')
def profile(request):
    return render (request, 'user/profile.html')

def base(request):
    return render (request, 'user/base.html')


def index2(request):
    print ('Hope its working')
    return render(request, 'user/index2.html')

def loginuser(request):
    return render(request,"user/loginpage.html")
def verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check if user has entered correct credentials
        user = authenticate(email=email, password=password)
        if user is not None:
            # A backend authenticated the credentials.
            login(request, user)
            return redirect('/profile')
        else:
            messages.warning(request, 'Email or password is not correct')
            # No backend authenticated the credentials.
            return redirect('/login')

def awelcome(request):
    return render(request,'user/agentwelcome.html')

def takeme(request):
    return redirect('/members/agentoruser')
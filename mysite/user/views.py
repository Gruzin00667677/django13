from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from mysite import settings
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, UserPasswordChangeForm


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('index')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context=context)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):  # Параметр ?next руководит перенаправлением
    #     return reverse_lazy('index')


def user_logout(request):
    logout(request)
    return redirect('login')


def user_register(request):
    return render(request, 'user/register.html')


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user/profile.html'
    form_class = UserUpdateForm
    extra_context = {
        'title': 'Личный кабинет',
        'default_image_url': settings.DEFAULT_USER_IMAGE
    }

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'user/password_change_form.html'

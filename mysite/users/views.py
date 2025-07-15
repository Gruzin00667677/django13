from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView
from .forms import LoginForm, UserRegisterForm


# Create your views here.
# def login_view(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             return redirect('/users/')
#         return render(request, 'users/login.html')
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('/users/')
#
#     return render(request, 'users/login.html', {'error': 'Invalid'})
class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('index')


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

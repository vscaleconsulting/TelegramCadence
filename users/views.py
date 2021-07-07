from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, ListView

from . import forms, models


class UserCreateView(CreateView):
    template_name = 'users/user-create.html'
    form_class = forms.UserModelForm

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)

        user.save()

        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:home-page')


class UserDeleteView(DeleteView):
    template_name = 'users/user-delete.html'
    model = models.User
    success_url = reverse_lazy('core:home-page')


class UserListView(ListView):
    template_name = 'users/user-list.html'
    queryset = models.User.objects.filter(is_superuser=False)


class CustomLoginView(LoginView):
    template_name = 'users/user-login.html'

    def get_success_url(self):
        return reverse('core:home-page')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home-page')

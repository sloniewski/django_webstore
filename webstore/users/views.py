from django.contrib.auth.views import LoginView, LogoutView


class UsersLoginView(LoginView):
    template_name = 'users/login.html'


class UsersLogoutView(LogoutView):
    pass

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView

from webstore.cart.models import Cart

from .forms import AuthenticateSessionForm


class UsersLoginView(LoginView):
    template_name = 'users/login.html'


class UsersLogoutView(LogoutView):
    pass


class AuthenticateSession(FormView):
    form_class = AuthenticateSessionForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        retained_session_key = self.request.session.session_key
        print(retained_session_key)
        if user is not None:
            login(self.request, user)
        print(self.request.session.session_key)
        cart = Cart.objects.filter(session=retained_session_key).first()
        if cart is not None:
            cart.session = self.request.session.session_key
            cart.save()
        return HttpResponseRedirect('/product/list/')

    def get_success_url(self):
        return '/product/list/'

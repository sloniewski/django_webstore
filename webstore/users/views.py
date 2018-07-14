from django.shortcuts import redirect, reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView

from webstore.cart.models import Cart

from .forms import UserCreationForm


class UsersLoginView(LoginView):
    template_name = 'users/login.html'


class UsersLogoutView(LogoutView):
    pass


class LoginRegisterBaseView():
    form_class = None
    template_name = 'users/login.html'
    redirect_field_name = 'next'
    login_form = AuthenticationForm
    register_form = UserCreationForm

    extra_context = {
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    }

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)

    def get_success_url(self):
        redirect_url = self.request.GET.get(self.redirect_field_name)
        if redirect_url is None:
            return reverse('order:order-confirm')
        else:
            return reverse(redirect_url)

    def form_valid(self, form):
        user = form.get_user()
        retained_session_key = self.request.session.session_key

        if user is not None:
            login(self.request, user)

        cart = Cart.objects.filter(session=retained_session_key).first()
        if cart is not None:
            cart.session = self.request.session.session_key
            cart.save()
        return redirect(self.get_success_url())


class AuthenticateUserView(LoginRegisterBaseView, FormView):

    def get_form_class(self):
        return self.login_form

    def form_invalid(self, form):
        self.extra_context['login_form'] = form
        return self.render_to_response(self.get_context_data())


class RegisterUserView(LoginRegisterBaseView, FormView):

    def get_form_class(self):
        return self.register_form

    def form_invalid(self, form):
        self.extra_context['register_form'] = form
        return self.render_to_response(self.get_context_data())

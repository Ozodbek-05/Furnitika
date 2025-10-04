import threading
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from apps.accounts.tokens import account_activation_token
from apps.accounts.utils import send_email_confirmation
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib import messages
from apps.accounts.forms import RegisterModelForm, LoginForm
from django.utils.translation import gettext as _


class RegisterCreateView(CreateView):
    template_name = 'auth/user-register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        email_thread = threading.Thread(target=send_email_confirmation, args=(user, self.request,))
        email_thread.start()

        messages.success(
            self.request,
            _("We have sent a verification email to your address. Please check your inbox.")
        )
        return super().form_valid(form)


    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(self.request, error)
        return super().form_invalid(form)


class LoginFormView(FormView):
    template_name = 'auth/user-login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages:home')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        if user:
            login(self.request, user)
            messages.success(
                self.request,
                _("Welcome back! You are now logged in!"), extra_tags='logged'
            )
        return super().form_valid(form)


    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(self.request, error)
        return super().form_invalid(form)


class ConfirmEmailView(View):
    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            messages.error(request, "User not found")
            return redirect('accounts:login')

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your email address is verified!")
            return redirect('accounts:login')
        else:
            messages.error(request, "Link is not correct")
            return redirect('accounts:register')
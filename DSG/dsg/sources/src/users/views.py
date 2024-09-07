from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, ListView

from communications.views import email_to_customer
from users.forms import CustomUserCreationForm, UserUpdateForm
from users.models import CustomUser

from users.token import account_activation_token

__all__ = (
    'SignUpView',
    'UserUpdateView',
    'AllUsersView',
    'user_activate',
    'email_confirm_done'
)


class SignUpView(SuccessMessageMixin, CreateView):
    """
    Класс регистрации нового пользователя
    """
    form_class = CustomUserCreationForm
    template_name = 'signup.html'

    # success_message = "Регистрация прошла успешно."

    def get_success_url(self):
        return reverse("email_confirm_done")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        email = user.email
        user.save()
        # получаем адрес нашего сайта
        current_site = get_current_site(self.request)
        html_message = loader.render_to_string(
            'users/email_confirm_mail.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        subject = "Подтверждение E-mail"
        email_to_customer(subject, html_message, email)
        return super().form_valid(form)


def email_confirm_done(request):
    """
    Функция просмотра страницы об успешной отправке e-mail с подтверждением
    """
    return render(request, 'users/email_confirm_done.html')


def user_activate(request, uidb64, token):
    """
    Функция активации пользователя после подтверждения e-mail
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        e_mail = user.email
        user_count = CustomUser.objects.all().count()
        user.save()

        return render(request, 'users/email_confirm_complete.html')
    else:
        return render(request, 'users/email_confirm_denied.html')


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Класс обновления данных пользователя
    """
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/account.html'
    success_url = reverse_lazy('account')
    success_message = "Данные успешно обновлены."

    def get_object(self, **kwargs):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.save()
        return super().form_valid(form)


class AllUsersView(LoginRequiredMixin, ListView):
    """
    Класс просмотра информации обо всех пользователях.
    Внимание! Просмотр доступен только Суперпользователям.
    """
    model = CustomUser

    def get_template_names(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            template_name = 'users/all_users.html'
        else:
            template_name = 'access_denied.html'
        return template_name

    def get_context_data(self, **kwargs):
        context = super(AllUsersView, self).get_context_data(**kwargs)
        context["all_users"] = CustomUser.objects.all()
        return context

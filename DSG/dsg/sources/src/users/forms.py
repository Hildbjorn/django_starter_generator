from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser, Ranks


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    """
    error_messages = {
        'password_mismatch': ('Введенные пароли не совпадают',),
    }

    email = forms.EmailField(label='E-mail:',
                             required=True,
                             widget=forms.TextInput(attrs={'id': 'id_username',
                                                           'aria-describedby': 'emailHelp'}, ),
                             error_messages={'unique': ("Пользователь с таким e-mail уже зарегистрирован",)})

    password1 = forms.CharField(label='Пароль:',
                                strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'new-password',
                                                                  'aria-describedby': 'password1Help'}),
                                help_text=password_validation.password_validators_help_text_html(),
                                )
    password2 = forms.CharField(label='Пароль еще раз:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'new-password',
                                                                  'aria-describedby': 'password2Help'}),
                                strip=False,
                                help_text="Введите тот же пароль, что ввели выше.",
                                )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password1',
            'password2'
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Форма изменения пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ('email',)


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя в модели CustomUser.
    """

    last_name = forms.CharField(required=False,
                                label='Фамилия:',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'id': 'last_name',
                                                              'placeholder': 'Фамилия'}))

    first_name = forms.CharField(required=False,
                                 label='Имя:',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'id': 'first_name',
                                                               'placeholder': 'Имя'}))

    middle_name = forms.CharField(required=False,
                                  label='Отчество:',
                                  widget=forms.TextInput(attrs={'class': 'form-control ',
                                                                'id': 'middle_name',
                                                                'placeholder': 'Отчество'}))

    phone = forms.CharField(required=False,
                            label='Телефон:',
                            widget=forms.TextInput(attrs={'class': 'tel form-control',
                                                          'id': 'phone',
                                                          'placeholder': 'Телефон'}))

    email = forms.EmailField(label='E-mail:',
                             required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'id': 'email',
                                                           'placeholder': 'user@mail.ru'}),
                             error_messages={'unique': ("Пользователь с таким e-mail уже зарегистрирован"),
                                             'invalid': ("Введите корректное значение")})

    company = forms.CharField(required=False,
                              label='Компания:',
                              widget=forms.TextInput(attrs={'id': 'company',
                                                            'name': 'company',
                                                            'onselect': 'findCompany()',
                                                            'class': 'form-control company_field',
                                                            'placeholder': 'Компания (введите название)'}))

    position = forms.CharField(required=False,
                               label='Должность:',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'position',
                                                             'placeholder': 'Должность'}))

    rank = forms.ModelChoiceField(required=False,
                                  label='Позиция в компании:',
                                  queryset=Ranks.objects.all(),
                                  empty_label="Выберите ранг",
                                  widget=forms.Select(attrs={'class': 'form-select form-control',
                                                             'id': 'rank'}))

    agreement = forms.BooleanField(required=True,
                                   label='',
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                     'type': 'checkbox',
                                                                     'role': 'switch',
                                                                     'id': 'agreement',
                                                                     'checked': ''}))

    class Meta:
        model = CustomUser
        fields = (
            'last_name',
            'first_name',
            'middle_name',
            'phone',
            'email',
            'company',
            'position',
            'rank',
            'agreement',
        )

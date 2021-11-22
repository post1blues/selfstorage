from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('fullname', 'email', 'pure_phonenumber', 'address', 'passport_code')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('fullname', 'email', 'pure_phonenumber', 'address')
        labels = {
            'fullname': 'ФИО',
            'pure_phonenumber': 'Телефон',
            'email': 'Электронная почта',
            'passport_code': 'Код паспорта'
        }
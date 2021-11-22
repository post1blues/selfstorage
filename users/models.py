from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField




class CustomUser(AbstractUser):
    """кастомный пользователь системы """
    fullname = models.CharField(verbose_name="ФИО", max_length=200)
    phonenumber = PhoneNumberField(verbose_name="нормализированный номер телефона", blank=True)
    pure_phonenumber = models.CharField(verbose_name="номер телефона", max_length=20)
    address = models.CharField(verbose_name="адрес", max_length=100)
    email = models.EmailField(verbose_name="электронная почта", max_length=255, unique=True)
    is_active = models.BooleanField('active', default=True)
    created_at = models.DateTimeField(verbose_name='дата создания', default=timezone.now)
    passport_code = models.CharField(verbose_name='код пасспорта', max_length=40)
    qr_code = models.ImageField(verbose_name='qr-код', upload_to='qr_codes/', null=True)

    username = models.CharField(
        'username',
        max_length=150,
        blank=True,
        null=True,
    )

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'pure_phonenumber', 'address', 'username']
    objects = UserManager()

    def get_full_name(self):
        return f'{self.fullname} - {self.email}'

    def get_short_name(self):
        """Return the short name for the user."""
        return self.fullname

    def __str__(self):
        return f"{self.fullname}"

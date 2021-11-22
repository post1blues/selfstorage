from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from users.models import CustomUser as Customer


class Storage(models.Model):
	title = models.CharField(verbose_name="название", max_length=20)
	address = models.CharField(verbose_name="адрес", max_length=100)
	price = models.DecimalField(
		verbose_name="цена",
		max_digits=8,
		decimal_places=2,
		validators=[MinValueValidator(0.01)]
	)
	created_at = models.DateTimeField(default=timezone.now, verbose_name="дата добавления")

	class Meta:
		verbose_name = 'склад'
		verbose_name_plural = 'склады'

	def __str__(self):
		return self.title


class Box(models.Model):
	title = models.CharField(verbose_name="наименование контейнера", max_length=20)
	size = models.PositiveIntegerField(
		verbose_name="размер контейнера",
	)
	price = models.DecimalField(
		verbose_name="цена аренды",
		max_digits=8,
		decimal_places=2,
		validators=[MinValueValidator(0.01)]
	)
	created_at = models.DateTimeField(verbose_name="дата добавления", default=timezone.now)

	class Meta:
		verbose_name = "контейнер"
		verbose_name_plural = "контейнеры"

	def __str__(self):
		return f"{self.title}"


class Payment(models.Model):
	card_number = models.PositiveIntegerField(default=0)
	price = models.DecimalField(
		verbose_name="сумма",
		max_digits=8,
		decimal_places=2,
		validators=[MinValueValidator(0.00)]
	)
	created_at = models.DateTimeField(verbose_name="дата создания платежа", default=timezone.now)
	updated_at = models.DateTimeField(verbose_name="дата обновления платежа", default=timezone.now)
	is_success = models.BooleanField(verbose_name="статус оплаты", default=False)

	class Meta:
		verbose_name = "платёж"
		verbose_name_plural = "платежи"

	def __str__(self):
		return f"{self.price} {self.created_at}"


class SeasonService(models.Model):
	title = models.CharField(verbose_name="название товара", max_length=20)
	image = models.ImageField(upload_to="images/", null=True)
	price_per_week = models.DecimalField(
		verbose_name="цена хранения на неделю",
		max_digits=8,
		decimal_places=2,
		validators=[MinValueValidator(0.00)]
	)
	price_per_month = models.DecimalField(
		verbose_name="цена хранения на месяц",
		max_digits=8,
		decimal_places=2,
		validators=[MinValueValidator(0.00)]
	)
	created_at = models.DateTimeField(verbose_name="дата добавления", default=timezone.now)

	class Meta:
		verbose_name = "сезонная вещь"
		verbose_name_plural = "сезонные вещи"

	def __str__(self):
		return f"{self.title}"


class BaseOrder(models.Model):
	customer = models.ForeignKey(
		Customer,
		verbose_name="клиент",
		related_name="order",
		null=True,
		on_delete=models.SET_NULL
	)
	storage = models.ForeignKey(
		Storage,
		verbose_name="склад",
		related_name="order",
		null=True,
		on_delete=models.SET_NULL
	)
	price = models.DecimalField(
		verbose_name="стоимость заказа",
		max_digits=8,
		decimal_places=2,
		validators=[MinValueValidator(0.00)]
	)
	created_at = models.DateTimeField(verbose_name="дата создания", default=timezone.now)
	payment = models.OneToOneField(
		Payment,
		verbose_name="платёж",
		related_name="order",
		on_delete=models.CASCADE,
		null=True
	)
	start_of_storage = models.DateField(
		verbose_name="дата окончания хранения",
		default=timezone.now
	)
	end_of_storage = models.DateField(
		verbose_name="дата окончания хранения"
	)

	class Meta:
		verbose_name = "заказ"
		verbose_name_plural = "заказы"

	def __str__(self):
		return f'{self.id} - {self.created_at}'


class StorageOrder(BaseOrder):
	box = models.ForeignKey(Box, related_name='order', on_delete=models.SET_NULL, null=True, verbose_name='бокс')

	class Meta:
		verbose_name = 'заказ бокса'
		verbose_name_plural = 'заказы боксов'


class SeasonOrder(BaseOrder):
	season_product = models.ForeignKey(
		SeasonService,
		related_name='order',
		on_delete=models.SET_NULL,
		null=True,
		verbose_name='что на хранении'
	)

	class Meta:
		verbose_name = 'сезонное хранение'
		verbose_name_plural = 'сезонное хранение'

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

PRODUCT_IMAGE_UPLOAD_TO = 'products/'

STATUS_CHOICES = (
    ('new', 'Новый'),
    ('completed', 'Завершен'),
)

ROLE_CHOICES = [
    ('admin', 'Администратор'),
    ('manager', 'Менеджер'),
    ('client', 'Авторизированный клиент'),
]


class Profile(models.Model):
    """Расширение модели User: ФИО и роль."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name='ФИО'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name='Роль'
    )

    def __str__(self):
        return self.full_name or self.user.username

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаёт профиль при создании пользователя."""
    if created:
        full_name = f"{instance.first_name} {instance.last_name}".strip()
        if not full_name:
            full_name = instance.username
        Profile.objects.create(
            user=instance, full_name=full_name, role='client')


class Category(models.Model):
    """Категория товара."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='URL-идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Производитель товара."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Производитель'
    )

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Поставщик товара."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Поставщик'
    )

    class Meta:
        verbose_name = 'поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Unit(models.Model):
    """Единица измерения товара."""
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар (обувь)."""
    article = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Артикул',
        validators=[
            RegexValidator(
                r'^[A-Z0-9]+$',
                'Артикул содержит только заглавные латинские буквы и цифры.'
            )
        ]
    )
    name = models.CharField(
        max_length=64,
        verbose_name='Наименование',
        db_index=True
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Единица измерения'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Поставщик'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Производитель'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Скидка (%)'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество на складе'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to=PRODUCT_IMAGE_UPLOAD_TO,
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Рекомендуемый размер 300x200 пикселей.'
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.article})'


class PickupPoint(models.Model):
    """Пункт выдачи заказов."""
    address = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Адрес пункта выдачи'
    )

    class Meta:
        verbose_name = 'пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'

    def __str__(self):
        return self.address


class Order(models.Model):
    """Заказ клиента."""
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер заказа',
        validators=[
            RegexValidator(
                r'^\d+$',
                'Номер заказа должен содержать только цифры.'
            )
        ],
        db_index=True
    )
    order_date = models.DateField(
        verbose_name='Дата заказа'
    )
    delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата доставки'
    )
    pickup_point = models.ForeignKey(
        PickupPoint,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Пункт выдачи'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Клиент'
    )
    pickup_code = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Код получения',
        validators=[
            RegexValidator(
                r'^\d+$',
                'Код получения должен содержать только цифры.'
            )
        ],
        db_index=True
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
        db_index=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):
        return f'Заказ №{self.order_number}'


class OrderItem(models.Model):
    """Позиция заказа (связь заказа и товара)."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена на момент заказа'
    )

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


CONTACT_TYPE_CHOICES = [
    ('supplier', 'Поставщик'),
    ('shop', 'Магазин'),
]

ORDER_STATES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Базовый класс для реализации объекта пользователя
    """
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)

    username = models.CharField(max_length=150,
                                verbose_name='Имя пользователя',
                                unique=True, blank=False)
    email = models.EmailField(verbose_name='email пользователя',
                              unique=True, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        ordering = ('username',)


class Company(models.Model):
    """
    Класс для реализации объекта Компания (поставщик, магазин)
    """
    company_name = models.CharField(verbose_name='Название компании',
                                    max_length=50, null=True, blank=True)
    type = models.CharField(verbose_name='Тип компании', blank=True,
                            choices=CONTACT_TYPE_CHOICES, max_length=10,
                            default='shop')
    url = models.URLField(verbose_name='Ссылка на сайт компании', null=True,
                          blank=True)
    filename = models.CharField(verbose_name='Файл', max_length=50,
                                null=True, blank=True)

    def __str__(self):
        return (f'{self.id}-{self.company_name}')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Список компаний'
        ordering = ('company_name',)
#

class Category(models.Model):
    """
    Класс для реализации объекта Категория продуктов
    """
    name = models.CharField(verbose_name='Название категории', max_length=50)
    company = models.ManyToManyField(Company, verbose_name='Компании',
                                   related_name='categories', blank=True)

    def __str__(self):
        return (f'{self.id}-{self.name}')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Список категорий'
        ordering = ('name',)


class Product(models.Model):
    """
    Класс для реализации объекта Продукт
    """
    name = models.CharField(verbose_name='Название продукта', max_length=50)
    category = models.ForeignKey(Category, verbose_name='Категория продукта',
                                 related_name='products', blank=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.id}-{self.name}')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Список продуктов'
        ordering = ('name',)


class ProductInfo(models.Model):
    """
    Класс для реализации объекта Информация о продукте
    """
    product = models.ForeignKey(Product, verbose_name='Продукт',
                                related_name='product_infos',
                                blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name='Компания', blank=True,
                             related_name='product_infos',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Информация', max_length=50)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая цена')

    def __str__(self):
        return (f'{self.id}-{self.name}-{self.quantity}-{self.price}')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информационный список о продуктах'
        ordering = ('name',)


class Parameter(models.Model):
    """
    Класс для реализации объекта Параметр
    """
    name = models.CharField(verbose_name='Название параметра', max_length=50)

    def __str__(self):
        return (f'{self.id}-{self.name}')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Список параметров'
        ordering = ('name',)


class ProductParameter(models.Model):
    """
    Класс для реализации объекта Параметр продукта
    """
    product_info = models.ForeignKey(ProductInfo,
                                     related_name='product_parameters',
                                     verbose_name='Информация о продукте',
                                     blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter,
                                  related_name='product_parameters',
                                  verbose_name='Параметр',
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    def __str__(self):
        return str(f'{self.id}-{self.parameter.name}-{self.value}')

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Список параметров продукта'
        ordering = ('value',)


class Order(models.Model):
    """
    Класс для реализации объекта Заказ
    """
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=50,
                              choices=ORDER_STATES, default='basket')

    def __str__(self):
        return str(f'{self.register_date} {self.status}')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'
        ordering = ('-register_date',)


class OrderItem(models.Model):
    """
    Класс для реализации объекта Позиция заказа
    """
    order = models.ForeignKey(Order, verbose_name='Заказ',
                              related_name='ordered_items',
                              blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт',
                                related_name='ordered_items',
                                blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name='Компания',
                             related_name='ordered_items',
                             blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return str(f'{self.id}-{self.order.id}-{self.product.name}-'
                   f'{self.quantity}')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'


class Contact(models.Model):
    """
    Класс для реализации объекта Контакт (пользователя)
    """
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=False,
                             on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', blank=True,
                             max_length=50)
    company = models.ForeignKey(Company, verbose_name='Компания',
                                related_name='contacts', blank=True,
                                on_delete=models.CASCADE)
    position = models.CharField(verbose_name='Должность',
                                blank=True, max_length=50)
    phone = models.CharField(max_length=20, verbose_name='Телефон',
                             blank=True)



    def __str__(self):
        return str(f'{self.user.username} {self.type}')

    class Meta:
        verbose_name = 'Тип контакта пользователя'
        verbose_name_plural = 'Типы контактов пользователей'
        ordering = ('user',)
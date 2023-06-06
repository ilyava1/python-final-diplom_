from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class User(AbstractUser):
    username = models.CharField(max_length=150,
                                verbose_name='Имя пользователя', unique=True)
    email = models.EmailField(verbose_name='email пользователя', unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('username',)


class Shop(models.Model):
    name = models.CharField(verbose_name='Название магазина', max_length=50)
    url = models.URLField(verbose_name='Ссылка на сайт магазина', null=True,
                          blank=True)
    filename = models.CharField(verbose_name='Файл', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=50)
    shops = models.ManyToManyField(Shop, verbose_name='Магазины',
                                   related_name='categories', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(verbose_name='Название продукта', max_length=50)
    category = models.ForeignKey(Category, verbose_name='Категория продукта',
                                 related_name='products', blank=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Список продуктов"
        ordering = ('name',)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт',
                                related_name='product_infos',
                                blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', blank=True,
                             related_name='product_infos',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Информация', max_length=50)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информационный список о продуктах"
        ordering = ('name',)


class Parameter(models.Model):
    name = models.CharField(verbose_name='Название параметра', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"
        ordering = ('name',)


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo,
                                     related_name='product_parameters',
                                     verbose_name='Информация о продукте',
                                     blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, related_name='product_parameters',
                                  verbose_name='Параметр',
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    def __str__(self):
        return str(f'{self.parameter.name} {self.value}')

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = "Список параметров продукта"
        ordering = ('value',)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=50)

    def __str__(self):
        return str(f'{self.dt} {self.status}')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"
        ordering = ('-register_date',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ',
                              related_name='ordered_items',
                              blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт',
                                related_name='ordered_items',
                                blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин',
                             related_name='ordered_items',
                             blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return str(f'{self.product.name} {self.quantity}')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = "Список позиций заказа"


class Contact(models.Model):
    type = models.CharField(verbose_name='Тип контакта', max_length=50)
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=50)
    type = models.CharField(max_length=5, default='Покупатель')

    def __str__(self):
        return str(f'{self.user.name} {self.type}')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"
        ordering = ('type',)
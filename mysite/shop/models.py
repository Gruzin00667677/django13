from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Brand(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=7, default=0.00, decimal_places=2, verbose_name="Цена")
    created = models.DateField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Категория", related_name='products')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED, verbose_name='Статус')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.title


class Rubric(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'
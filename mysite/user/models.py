from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True , verbose_name='Фото')
    phone = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name='Телефон')
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

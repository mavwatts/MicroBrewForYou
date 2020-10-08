from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=280, default='')
    user_image = models.ImageField(
        upload_to='CustomUser/', null=False, blank=False)
    users_following = models.ManyToManyField(
        "self", symmetrical=False, related_name='CustomUser')
    fav_breweries = models.ManyToManyField(
        "Breweries", symmetrical=False,
        related_name='fav_breweries', blank=True)
    fav_brewtypes = models.ManyToManyField(
        "BrewTypes", symmetrical=False,
        related_name='fav_brewtypes', blank=True)
    address = models.CharField(max_length=280)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['first_name', 'bio', 'address', 'city', 'state']

    def __str__(self):
        return self.username


class Posts(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='author')
    body = models.TextField(max_length=280)
    postTime = models.DateTimeField(default=timezone.now)
    lastUpdated = models.DateField(auto_now=True)

    def __str__(self):
        return self.body


class Breweries(models.Model):
    name = models.CharField(max_length=80)
    city = models.TextField(max_length=240)
    address = models.TextField(max_length=240, default='')
    website = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class BrewTypes(models.Model):
    name = models.CharField(max_length=80)
    averageABV = models.FloatField()

    def __str__(self):
        return self.name

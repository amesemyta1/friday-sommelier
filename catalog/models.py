from django.contrib.auth.models import AbstractUser
from django.db import models


class AlcoholType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Flavor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Snack(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_cooking_required = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Taster(AbstractUser):
    class Experience(models.IntegerChoices):
        BEGINNER = 1, "Beginner"
        AMATEUR = 2, "Amateur"
        SOMMELIER = 3, "Sommelier"

    experience_level = models.IntegerField(
        choices=Experience.choices, default=Experience.BEGINNER
    )
    preferred_flavors = models.ManyToManyField(
        Flavor, blank=True, related_name="tasters"
    )
    favorite_beverages = models.ManyToManyField(
        "Beverage",
        blank=True,
        related_name="favorite_by",
        verbose_name="Favorite Beverages",
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username


class Beverage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    alcohol_strength = models.FloatField()
    alcohol_type = models.ForeignKey(
        AlcoholType, on_delete=models.CASCADE, related_name="beverages"
    )
    tasters = models.ManyToManyField(
        Taster, blank=True, related_name="beverages"
    )
    snacks = models.ManyToManyField(
        Snack, blank=True, related_name="beverages"
    )
    flavors = models.ManyToManyField(
        Flavor, blank=True, related_name="beverages"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.alcohol_strength}%)"

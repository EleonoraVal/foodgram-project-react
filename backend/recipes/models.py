from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=30, unique=True, null=True)
    amount = models.IntegerField(default=0)
    unit = models.TextField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.amount}, {self.unit}'
    

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True, default='0000FF')
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True)
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    image = models.ImageField(upload_to='recipes/',
        blank=True,
        null=True)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)
    cooking_time = models.IntegerField(default=0)

    def __str__(self):
        return self.name

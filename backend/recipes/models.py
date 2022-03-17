from django.db import models
from users.models import User


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
    ingredient = models.ManyToManyField(Ingredient, related_name='recipes')
    tag = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_list'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe'
            )
        ]

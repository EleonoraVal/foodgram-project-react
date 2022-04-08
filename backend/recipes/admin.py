from django.contrib import admin
from users.models import User

from .models import (Favorite, Follow, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time')
    search_fields = ('text',)
    list_filter = ('name', 'author', 'tags')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    ordering = ('id',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    ordering = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class FavoriteAdmin(admin.ModelAdmin):
    pass


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)

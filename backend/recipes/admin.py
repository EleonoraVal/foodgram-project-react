from csv import list_dialects
from django.contrib import admin
from .models import Recipe, Tag, Ingredient, Follow

from users.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time')
    search_fields = ('text',)
    list_filter = ('name', 'author', 'tag')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    ordering = ('id',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'unit')
    ordering = ('name',)

class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)

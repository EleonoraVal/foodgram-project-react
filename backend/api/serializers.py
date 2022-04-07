from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from recipes.models import (Recipe, Tag, Ingredient,
                            Follow, Favorite, ShoppingCart, IngredientRecipe)
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='ingredient_amount'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'author',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(recipe=obj, user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(recipe=obj, user=user).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='ingredient_amount'
    )
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time'
        )

    def validate(self, data):
        ingredients_data = self.initial_data.get('ingredients')
        ingredients_unique_list = []
        for ingredient in ingredients_data:
            if int(ingredient['amount']) < 1:
                raise serializers.ValidationError(
                    'Количество должно быть больше 0!'
                )
            ingredient_to_check = get_object_or_404(Ingredient,
                                                    id=ingredient['id']
                                                    )
            if ingredient_to_check in ingredients_unique_list:
                raise serializers.ValidationError(
                    'Повтор ингредиентов')
            ingredients_unique_list.append(ingredient_to_check)
        data['ingredients'] = ingredients_data
        return data

    def create(self, validated_data):
        author = self.context['request'].user
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author,
                                       image=image,
                                       **validated_data)
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        for ingredient in ingredients_data:
            id = ingredient.get('id')
            amount = int(ingredient.get('amount'))
            IngredientRecipe.objects.create(
                ingredient_id=id,
                recipe=recipe,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.tags.clear()
        instance.tags.set(tags_data)
        for ingredient in ingredients_data:
            id, amount = ingredient['id'], ingredient['amount']
            ingredient_to_add = get_object_or_404(Ingredient, id=id)
            IngredientRecipe.objects.create(
                ingredient=ingredient_to_add,
                recipe=instance, amount=amount
            )
        instance.save()
        return instance


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email')
    id = serializers.EmailField(source='author.id')
    username = serializers.EmailField(source='author.username')
    first_name = serializers.EmailField(source='author.first_name')
    last_name = serializers.EmailField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_subscribed')
    recipes_count = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_recipes_count')
    recipes = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_recipes')

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(
                user=user, author=obj.author
            ).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context['recipes_limit']
        if recipes_limit:
            recipes = obj.author.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.author.recipes.all()
        return FavoriteRecipeSerializer(recipes, many=True).data


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, obj):
        user = obj['user']
        author = obj['author']
        request_method = self.context.get('request').method
        subscribed = Follow.objects.filter(
            user=user, author=author).exists()
        if subscribed and request_method == 'POST':
            raise ValidationError('На этого автора уже есть подписка!')
        if not subscribed and request_method == 'DELETE':
            raise ValidationError('На этого автора подписки не было!')
        return obj


class ShoppingCartSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            recipe_id = self.context['view'].kwargs.get('id')
            recipe = get_object_or_404(Recipe, id=recipe_id)
            if ShoppingCart.objects.filter(
                                           user=request.user,
                                           recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Рецепт уже есть в списке покупок!'
                )
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                                               user=request.user,
                                               recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Рецепт не был в списке покупок!'
                )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        recipe_id = self.context['view'].kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.create(user=user, recipe=recipe_id)
        return recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            recipe_id = self.context['view'].kwargs.get('id')
            recipe = get_object_or_404(Recipe, id=recipe_id)
            if Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                raise ValidationError('Рецепт уже в избранном!')
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                raise ValidationError('Рецепт не был в списке избранного!')
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        recipe_id = self.context['view'].kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorite.create(user=user, recipe=recipe_id)
        return recipe


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

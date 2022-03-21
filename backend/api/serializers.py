from recipes.models import Recipe, Tag, Ingredient, Follow, Favorite, ShoppingCart
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'slug', 'color')


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    ingredient = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'author', 'image', 'ingredient', 'tag', 'cooking_time')

    # def create(self, instance, **validated_data):
    #     tag = validated_data.pop('tag')
    #     # recipe = Recipe.objects.create(**validated_data)
    #     # # recipe.tag.set(tag)
    #     for tags in tag:
    #         current_tag = Tag.objects.get_or_create(**tags)
    #     instance.tags.add(current_tag)
    #     return instance

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Подписка уже была оформлена!')
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        fields = ('id', 'name')
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('id', 'name')
            )
        ]

class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'recipe')
        model = ShoppingCart

from rest_framework import viewsets
from recipes.models import Recipe, Tag, Ingredient, Follow
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import IsOwnerOrReadOnly, IsAdmin

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, FollowSerializer,
                          FavoriteSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAdmin, ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     new_queryset = Follow.objects.filter(user=self.request.user)
    #     return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return self.request.user.favorite_recipe.all()

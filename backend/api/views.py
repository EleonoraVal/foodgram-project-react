from rest_framework import viewsets
from recipes.models import Recipe, Tag, Ingredient, Follow
from users.models import User
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from users.permissions import IsOwnerOrReadOnly

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, FollowSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


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

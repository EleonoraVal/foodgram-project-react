from django.shortcuts import render
from rest_framework import viewsets
from recipes.models import Recipe, Tag, Ingredient
from rest_framework.permissions import IsAuthenticated

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

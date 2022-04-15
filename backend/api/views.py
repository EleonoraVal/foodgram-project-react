from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Follow, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)

from .filters import (AuthorFilter, FavoriteFilter, ShoppingCartFilter,
                      TagFilter)
from .pagination import LimitPageSizePagination
from .permissions import IsAdminAuthorOrReadPost, IsAdminOrReadOnly
from .serializers import (FollowSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, TagSerializer, FavoriteSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadPost, )
    pagination_class = LimitPageSizePagination
    filter_backends = (TagFilter, AuthorFilter,
                       ShoppingCartFilter, FavoriteFilter)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated, ))
    def add_or_delete(self, request, model, serializer, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        is_already_added = model.objects.filter(user=user,
                                                recipe=recipe)
        if request.method == 'POST':
            if is_already_added:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                model.objects.create(user=user, recipe=recipe)
                serializer = serializer(
                    recipe, context={'request': request}
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED
                                )
        if request.method == 'DELETE':
            if is_already_added:
                follower_favorite = get_object_or_404(
                    model,
                    user=user,
                    recipe=recipe
                )
                follower_favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated, ))
    def favorite(self, request, pk):
        return self.add_or_delete(
            request,
            Favorite,
            FavoriteSerializer,
            pk
        )

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated, ))
    def shopping_cart(self, request, pk):
        return self.add_or_delete(
            request,
            ShoppingCart,
            FavoriteSerializer,
            pk
        )

    @staticmethod
    def canvas_method(shopping_list):
        begin_position_x, begin_position_y = 30, 730
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"')
        canvas = Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSans', 'data/fonts/FreeSans.ttf'))
        canvas.setFont('FreeSans', 25)
        canvas.setTitle('Список покупок')
        canvas.drawString(begin_position_x,
                          begin_position_y + 40, 'Список покупок: ')
        canvas.setFont('FreeSans', 18)
        for number, item in enumerate(shopping_list, start=1):
            if begin_position_y < 100:
                begin_position_y = 730
                canvas.showPage()
                canvas.setFont('FreeSans', 18)
            canvas.drawString(
                begin_position_x,
                begin_position_y,
                f'{number}: {item["ingredient__name"]} - '
                f'{item["ingredient_total"]}'
                f'{item["ingredient__measurement_unit"]}'
            )
            begin_position_y -= 30
        canvas.showPage()
        canvas.save()
        return response

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        return self.canvas_method(ingredients)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    pagination_class = LimitPageSizePagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(
            user=user).select_related('author')

    def get_serializer_context(self):
        recipes_limit = self.request.query_params.get('recipes_limit')
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'recipes_limit': recipes_limit
        }

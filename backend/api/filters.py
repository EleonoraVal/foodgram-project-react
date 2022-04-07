from rest_framework import filters


class TagFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        return queryset


class AuthorFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        author = request.GET.get('author')
        if author:
            return queryset.filter(author=author)
        return queryset


class FavoriteFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_favorited = request.GET.get('is_favorited')
        user = request.user
        if is_favorited != '1':
            return queryset
        if user.is_authenticated:
            return queryset.filter(following__user=user)
        return None


class ShoppingCartFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_in_shopping_cart = request.GET.get('is_in_shopping_cart')
        user = request.user
        if is_in_shopping_cart != '1':
            return queryset
        if user.is_authenticated:
            return queryset.filter(cart__user=user)
        return None

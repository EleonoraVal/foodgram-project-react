from django.urls import include, path
from rest_framework import routers
from .views import (RecipeViewSet, TagViewSet,
                    IngredientViewSet, FollowViewSet)
from users.views import UserViewSet

router = routers.DefaultRouter()
app_name = 'api'

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'users', UserViewSet, basename='users')
router.register(r'users/subscriptions',
                FollowViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

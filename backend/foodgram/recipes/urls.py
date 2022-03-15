from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('recipe/', views.recipe_list),
    path('recipe/<pk>/', views.recipe_detail),
]

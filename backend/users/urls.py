from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

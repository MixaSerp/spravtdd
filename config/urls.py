# config/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- добавили include!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # <-- теперь работает!
]
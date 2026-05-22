# app/urls.py
from django.urls import path
from .views import TermListView

urlpatterns = [
    path('', TermListView.as_view(), name='term_list'),
]
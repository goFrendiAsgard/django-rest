from django.urls import path
from .views import notes_pk, notes

urlpatterns = [
    path('notes/<str:pk>/', notes_pk),
    path('notes/', notes),
]
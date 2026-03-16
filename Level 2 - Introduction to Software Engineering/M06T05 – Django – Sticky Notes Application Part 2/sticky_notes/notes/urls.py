from django.urls import path
from . import views

# All the URL patterns for the notes app
# The Edit and Delete URLs include the note's id as a parameter to know which
# note to edit or delete
urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('new/', views.note_create, name='note_create'),
    path('edit/<int:pk>/', views.note_update, name='note_update'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
]

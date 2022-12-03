from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastrar, name="cadastrar"),
    path('agenda/', views.agenda, name="agenda"),
    path('update/<int:pk>/', views.update, name="update"),
    #path('view/<int:pk>/', views.view, name="view"),
    #path('edit/<int:pk>/', views.edit, name="edit"),
    #path('update/<int:pk>/', views.update, name="update"),
    path('delete/<int:pk>/', views.delete, name="delete"),
]

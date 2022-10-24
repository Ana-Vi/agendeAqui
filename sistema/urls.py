from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('registrese/', views.registra, name="registra"),
    path('create/', views.create, name="create"),
    path('home/', views.home, name="home"),
    path('entra/<int:pk>/', views.entra, name="entra"),
    #path('view/<int:pk>/', views.view, name="view"),
    #path('edit/<int:pk>/', views.edit, name="edit"),
    #path('update/<int:pk>/', views.update, name="update"),
    #path('delete/<int:pk>/', views.delete, name="delete"),
]
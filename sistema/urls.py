from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('cadastro/', views.cadastro, name="cadastro"),
    #path('create/', views.create, name="create"),
    #path('view/<int:pk>/', views.view, name="view"),
    #path('edit/<int:pk>/', views.edit, name="edit"),
    #path('update/<int:pk>/', views.update, name="update"),
    #path('delete/<int:pk>/', views.delete, name="delete"),
]
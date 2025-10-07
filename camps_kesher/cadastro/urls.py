from django.urls import path, include
from .import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path("usuarios/", views.UsuarioListCreate.as_view(), name="usuario-list"),
    path("usuarios/<int:pk>/", views.UsuarioDetail.as_view(), name="usuario-detail"),
    path("fisico/", views.FisicoListCreate.as_view(), name="fisico-list"),
    path("fisicos/<int:pk>/", views.FisicoDetail.as_view(), name="fisico-detail"),
]
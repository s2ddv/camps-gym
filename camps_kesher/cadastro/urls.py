from django.urls import path, include
from .import views
from .views import authView

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("usuarios/", views.UsuarioListCreate.as_view(), name="usuario-list"),
    path("usuarios/<int:pk>/", views.UsuarioDetail.as_view(), name="usuario-detail"),
    path("fisico/", views.FisicoListCreate.as_view(), name="fisico-list"),
    path("fisicos/<int:pk>/", views.FisicoDetail.as_view(), name="fisico-detail"),
]
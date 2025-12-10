from django.urls import path
from .views import (
    UsuarioListCreate,
    UsuarioDetail,
    LoginViewAPI,
    LogoutViewAPI,
    UserDetailAPI
)

urlpatterns = [
    path("", UsuarioListCreate.as_view(), name="usuario-list-create"),
    path("<int:pk>/", UsuarioDetail.as_view(), name="usuario-detail"),
    path("login/", LoginViewAPI.as_view(), name="login"),
    path("logout/", LogoutViewAPI.as_view(), name="logout"),
    path("me/", UserDetailAPI.as_view(), name="me"),
]

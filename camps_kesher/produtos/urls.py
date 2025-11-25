from django.urls import path
from .views import (
    CategoriaList, CategoriaDetail, ProdutoListCreate, ProdutoDetail
)

urlpatterns = [
    path("categorias/", CategoriaList.as_view()),
    path("categorias/<int:pk>/", CategoriaDetail.as_view()),
    path("produtos/", ProdutoListCreate.as_view()),
    path("produtos/<int:pk>/", ProdutoDetail.as_view()),


]
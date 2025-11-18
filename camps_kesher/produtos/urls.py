from django.urls import path
from .views import (
    CategoriaList, CategoriaDetail, ProdutoListCreate, ProdutoDetail,
    add_to_cart, view_cart, update_cart_item, remove_from_cart, clear_cart
)

urlpatterns = [
    path("categorias/", CategoriaList.as_view()),
    path("categorias/<int:pk>/", CategoriaDetail.as_view()),
    path("produtos/", ProdutoListCreate.as_view()),
    path("produtos/<int:pk>/", ProdutoDetail.as_view()),

    path("cart/add/", add_to_cart),
    path("cart/", view_cart),
    path("cart/update/", update_cart_item),
    path("cart/remove/", remove_from_cart),
    path("cart/clear/", clear_cart),
]

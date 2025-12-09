from django.urls import path
from .views import (
    CategoriaList, 
    CategoriaDetail, 
    ProdutoListCreate, 
    ProdutoDetail,
    add_to_cart, 
    view_cart, 
    update_cart_item, 
    delete_cart_item,  
    clear_cart, 
    ProdutoComVariacaoCreate
)

urlpatterns = [
    path("categorias/", CategoriaList.as_view()),
    path("categorias/<int:pk>/", CategoriaDetail.as_view()),
    path("produtos/", ProdutoListCreate.as_view()),
    path("produtos/<int:pk>/", ProdutoDetail.as_view()),

    path('produto-com-variacao/', ProdutoComVariacaoCreate.as_view(), name='produto-com-variacao'),

    path("cart/add/", add_to_cart),
    path("cart/", view_cart),
    path("cart/update/", update_cart_item),
    path("cart/remove/", delete_cart_item),  
    path("cart/clear/", clear_cart),
]
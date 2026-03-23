from django.urls import path

from .views import (OrderCreateView, OrderDeleteView, OrderListView,
                    OrderUpdateView, ProductCreateView, ProductDeleteView,
                    ProductListView, ProductUpdateView)

app_name = 'shoes'

urlpatterns = [
    path(
        'list/',
        ProductListView.as_view(),
        name='product_list'
    ),
    path(
        'product/create/',
        ProductCreateView.as_view(),
        name='product_create'
    ),
    path(
        'product/<int:pk>/edit/',
        ProductUpdateView.as_view(),
        name='product_edit'
    ),
    path(
        'product/<int:pk>/delete/',
        ProductDeleteView.as_view(),
        name='product_delete'
    ),

    path(
        'orders/',
        OrderListView.as_view(),
        name='order_list'
    ),
    path(
        'order/create/',
        OrderCreateView.as_view(),
        name='order_create'
    ),
    path(
        'order/<int:pk>/edit/',
        OrderUpdateView.as_view(),
        name='order_edit'
    ),
    path(
        'order/<int:pk>/delete/',
        OrderDeleteView.as_view(),
        name='order_delete'
    ),
]

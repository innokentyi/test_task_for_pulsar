from django.urls import path

from .views import ProductListView, ProductView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductView.as_view(), name='product'),
]

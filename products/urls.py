from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create-product/', CreateProductView.as_view(),
         name='create_product'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<int:product_id>/',
         ProductDetail.as_view(),
         name='product_detail'),
    path('<slug:category_slug>/', ProductByCategory.as_view(),
         name='product_by_category'),

]

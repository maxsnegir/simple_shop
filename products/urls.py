from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create-product/', CreateProductView.as_view(),
         name='create_product'),
    path('category/<slug:category_slug>/', ProductByCategory.as_view(),
         name='product_by_category'),

    path('brand/<slug:brand_slug>', ProductsByBrand.as_view(),
         name='product_by_brand'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<int:product_id>/',
         ProductDetail.as_view(),
         name='product_detail'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<int:product_id>/',
         include('comments.urls'),),

]

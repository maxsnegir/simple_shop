from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from cart.forms import CartAddProductForm
from .forms import CreateProduct
from .models import *


class Index(generic.ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.select_related('subcategory__category', ).all()


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_object(self, queryset=None):
        category = self.kwargs['category_slug']
        subcategory = self.kwargs['subcategory_slug']
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product,
                                    subcategory__category__slug=category,
                                    subcategory__slug=subcategory,
                                    id=product_id)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context


class ProductByCategory(generic.ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category = get_object_or_404(Category,
                                     slug=self.kwargs['category_slug'])
        return Product.objects.select_related(
            'subcategory__category', ).filter(
            subcategory__category__slug=category.slug).all()


class ProductsByBrand(ProductByCategory):
    template_name = 'products/products_by_brand.html'

    def get_queryset(self):
        return Product.objects.filter(
            brand__slug=self.kwargs['brand_slug']).select_related(
            'subcategory__category',).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = get_object_or_404(Brand, slug=self.kwargs['brand_slug'])
        context['brand'] = brand
        return context


class CreateProductView(generic.CreateView):
    form_class = CreateProduct
    template_name = 'products/create_product.html'

    def has_permissions(self):
        return self.request.user.is_authenticated and \
               self.request.user.role != 'user'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return redirect('index')
        return super(CreateProductView, self).dispatch(request, *args,
                                                       **kwargs)

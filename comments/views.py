from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.forms import CommentForm
from comments.models import Comment
from products.models import Product


@login_required
def add_comment(request, category_slug, subcategory_slug, product_id):
    product = get_object_or_404(Product, id=product_id,
                                subcategory__slug=subcategory_slug,
                                subcategory__category__slug=category_slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.product = product
        new_comment.author = request.user
        new_comment.save()
    return redirect(reverse('product_detail',
                            args=[category_slug, subcategory_slug,
                                  product_id]))

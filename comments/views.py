from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from comments.forms import CommentForm
from comments.models import Comment
from products.models import Product


@login_required
def comment_add(request, category_slug, subcategory_slug, product_id):
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


@login_required
def comment_delete(request, category_slug, subcategory_slug, product_id,
                   comment_id):
    comment = get_object_or_404(Comment, id=comment_id,
                                product__id=product_id)

    if request.user == comment.author:
        comment.delete()
    return redirect(reverse('product_detail',
                            args=[category_slug, subcategory_slug,
                                  product_id]))

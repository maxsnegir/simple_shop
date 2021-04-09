from django.shortcuts import render, redirect

from .forms import OrderCreateForm

from cart.cart import Cart
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    form = OrderCreateForm(request.POST or None, )
    if request.method == 'POST':
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    return render(request, 'order/create.html',
                  {'cart': cart, 'form': form,
                   'errors': form.errors})

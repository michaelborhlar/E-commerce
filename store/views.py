
# Create your views here.
# store/views.py
from django.shortcuts import render, redirect
from .models import Product, Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    order = Order.objects.create(user=request.user)
    
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
    
    cart_items.delete()  # Clear the cart after order is created

    return render(request, 'store/order_confirmation.html', {'order': order})

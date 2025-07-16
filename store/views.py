from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order

# ✅ Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# ✅ Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        # Create user
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


# ✅ Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # 🔄 Redirect to next page after login (if any)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')


# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('home')


# ✅ Add to Cart (only when logged in)
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


# ✅ View Cart
@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ✅ Checkout Page
@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']
        payment_method = request.POST['payment_method']

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            payment_method=payment_method
        )

        order.items.set(cart_items)
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('home')

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

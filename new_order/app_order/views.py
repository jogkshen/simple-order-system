from django.shortcuts import render, redirect
from app_order.models import Product, Order
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('login')  # Redirect to the user's profile or another page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('base')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url=user_login)
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)  
    order, created = Order.objects.get_or_create(user=request.user, product=product, status=False) #status function ko kaam yeha hunxa

    return redirect('cartlist')

def custom_logout(request):
    logout(request) 
    return redirect('base')

def cartlist(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'cartlist.html', {'user_orders': user_orders})

def product(request):
    product = Product.objects.all()
    return render (request, 'product.html', {'product': product})


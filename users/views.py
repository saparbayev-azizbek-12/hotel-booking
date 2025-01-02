from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, CustomUserEditForm
from hotel.models import Order
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get(
                    'next', 'home'
                )
                messages.success(request, f"Welcome, {username}!")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def profile(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user.id).order_by('-id')
        today = datetime.now()
        if request.method == 'POST':
            user_form = CustomUserEditForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
        else:
            user_form = CustomUserEditForm(instance=user)
        context = {
            'user': user,
            'orders': orders,
            'today': today.date(),
        }
        return render(request, 'users/profile.html', context)
    else:
        return redirect('login')


def profile_delete(request, order_id):
    if request.user.is_authenticated:
        user = request.user.id
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.delete()
        return redirect('profile')
    else:
        return redirect('login')
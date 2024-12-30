from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserEditForm
from .models import CustomUser
from hotel.models import Order
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

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

def profile(request, id):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=id)
        orders = Order.objects.filter(user=user)
        today = datetime.now()
        print(today.date())
        context = {
            'user': user,
            'orders': orders,
            'today': today.date(),
        }
        return render(request, 'users/profile.html', context)
    else:
        return redirect('login')
    
def profile_edit(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            form = UserEditForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

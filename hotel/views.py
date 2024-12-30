from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Room, Order, Facilities
from django.contrib import messages
from urllib.parse import urlencode
from datetime import datetime

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def contact(request):
    return render(request, 'contact.html')

def booking(request):
    temporary = Order.objects.filter(user=request.user).last()
    rooms = Room.objects.all()
    return render(request, 'booking.html', {'order': temporary, 'rooms': rooms})

def gallery(request):
    return render(request, 'gallery.html')


def room_list(request):
    rooms = Room.objects.all()


    adults_ = 0
    children_ = 0
    if request.method == 'GET':
        checkin = request.POST.get('checkin', '')
        checkout = request.POST.get('checkout', '')
        adults_ = request.POST.get('adults', '')
        children_ = request.POST.get('children', '')

    if adults_ and children_:
        rooms = rooms.filter(adults__gte=int(adults_))
        rooms = rooms.filter(children__gte=int(children_))
    elif adults_:
        rooms = rooms.filter(adults_gte=int(adults_))

    filter_type = request.GET.get('filter_type')

    if filter_type == "standart":
        rooms = rooms.filter(room_type='standart')
    elif filter_type == "lux":
        rooms = rooms.filter(room_type='lux')
    elif filter_type == "econom":
        rooms = rooms.filter(room_type='economy')

    return render(request, 'room.html', {'rooms': rooms})


def room_detail(request, room_id):
    user = request.user
    room = get_object_or_404(Room, id=room_id)
    facilities = Facilities.objects.filter(room=room).first()

    if request.method == 'POST':
        if user.is_authenticated:
            username = user
            checkin = request.POST.get('checkin', '').strip()
            checkout = request.POST.get('checkout', '').strip()
            adults_ = request.POST.get('adults', '').strip()
            children_ = request.POST.get('children', '').strip()
            price = str(request.POST.get('room_price', '')).replace(',', '')
            print("checkin : ", checkin)
            print("checkout : ", checkout)
            print(f"price: {price}")

            try:
                if checkin:
                    checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
                if checkout:
                    checkout = datetime.strptime(checkout, '%Y-%m-%d').date()

                if checkin and checkout and checkin >= checkout:
                    messages.error(request, 'Check-out date must be after Check-in date.')
                    return render(request, 'room_detail.html', {'rooms': room, 'facilities': facilities})

                if not adults_ or not adults_.isdigit() or int(adults_) < 1:
                    messages.error(request, 'Please provide a valid number of adults.')
                    return render(request, 'room_detail.html', {'rooms': room, 'facilities': facilities})
                
                if not children_ or not children_.isdigit() or int(children_) < 0:
                    messages.error(request, 'Please provide a valid number of children.')
                    return render(request, 'room_detail.html', {'rooms': room, 'facilities': facilities})
                
                days = (checkout - checkin).days
                total = days*int(price)
                print(f"days: {days}")
                print(f"total: {total}")


                order = Order.objects.create(
                    user = user,
                    room = room,
                    checkin_date=checkin,
                    checkout_date=checkout,
                    number_of_adults=int(adults_),
                    number_of_children=int(children_),
                    total_price = int(total)
                )
                order.save()

                messages.success(request, 'Booking successful!')
                return redirect('room_detail', room_id=room.id)

            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
        else:
            messages.warning(request, 'You do not have an account!')
            return redirect('login')

    return render(request, 'room_detail.html', {'rooms': room, 'facilities': facilities})


def checkout(request):
    if not request.user.is_authenticated:
        next = request.build_absolute_uri()
        base_url = reverse('login')
        return redirect(f"{base_url}?{urlencode({'next': next})}")


def cancel_booking(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Booking has been successfully cancelled.")
    return redirect('order_history')

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Room, Order, Facilities
from django.contrib import messages
from urllib.parse import urlencode
from datetime import datetime
from django.db.models import Q

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
    orders = Order.objects.all()


    adults_ = 0
    children_ = 0
    if request.method == 'GET':
        checkin = request.GET.get('checkin', '')
        checkout = request.GET.get('checkout', '')
        adults_ = request.GET.get('adults', '')
        children_ = request.GET.get('children', '')

    if checkin and checkout:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')

        unavailable_rooms = orders.filter(
            Q(checkin_date__lt=checkout_date) & Q(checkout_date__gt=checkin_date)
        ).values_list('room_id', flat=True)

        rooms = rooms.exclude(id__in=unavailable_rooms)

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

            if checkin:
                checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
            if checkout:
                checkout = datetime.strptime(checkout, '%Y-%m-%d').date()

            try:
                if checkin and checkout and checkin >= checkout:
                    checkin = datetime.strptime(checkin, '%Y-%m-%d')
                    checkout = datetime.strptime(checkout, '%Y-%m-%d')

                    if Q(checkin_date__lt=checkout) & Q(checkout_date__gt=checkin):
                        print(True, Q(checkin_date__lt=checkout))
            except:
                messages.error(request, 'Check-out date must be after Check-in date.')
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
            return redirect('profile')

        else:
            messages.warning(request, 'You do not have an account!')
            return redirect('login')

    return render(request, 'room_detail.html', {'rooms': room, 'facilities': facilities})


def checkout(request):
    if not request.user.is_authenticated:
        next = request.build_absolute_uri()
        base_url = reverse('login')
        return redirect(f"{base_url}?{urlencode({'next': next})}")

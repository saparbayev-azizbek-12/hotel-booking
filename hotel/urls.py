from django.urls import path
from hotel import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('gallery/', views.gallery, name='gallery'),
    path('rooms/', views.room_list, name='room_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
]

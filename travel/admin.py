from django.contrib import admin
from .models import *

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'price', 'duration', 'is_available')
    list_filter = ('country', 'tour_type', 'is_available')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'tour', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published')
    search_fields = ('author', 'text')

@admin.register(EarlyBooking)
class EarlyBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tour', 'booking_date', 'is_processed')
    list_filter = ('is_processed', 'booking_date')

@admin.register(Visa)
class VisaAdmin(admin.ModelAdmin):
    list_display = ('country', 'processing_time', 'cost', 'is_available')
    list_filter = ('is_available', 'country')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'created_at')

#Регистрируем модели Ticket и связанные
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('type', 'departure_city', 'arrival_city', 'departure_date', 'price', 'available_seats', 'is_available')
    list_filter = ('type', 'is_available', 'departure_date')
    search_fields = ('departure_city', 'arrival_city')
    date_hierarchy = 'departure_date'


@admin.register(TicketBooking)
class TicketBookingAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'ticket', 'user', 'order_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'order_date')
    search_fields = ('passenger_name', 'passenger_email', 'passenger_phone')
    raw_id_fields = ('ticket', 'user')


@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'ticket', 'user', 'order_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'order_date')
    search_fields = ('passenger_name', 'passenger_email', 'passenger_phone')
    raw_id_fields = ('ticket', 'user')

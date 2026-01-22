from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('tours/', views.TourListView.as_view(), name='tour_list'),
    path('tours/<int:pk>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('add-review/', views.add_review, name='add_review'),
    path('visas/', views.VisaView.as_view(), name='visas'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
# Билеты
    path('tickets/<str:type>/', views.TicketListView.as_view(), name='tickets'),
    path('ticket/book/<int:ticket_id>/', views.book_ticket, name='book_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
# API для проверки
    path('api/check-auth/', views.check_auth, name='check_auth'),
# Корзина
path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),  # ОБЩАЯ ФУНКЦИЯ
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/checkout/', views.checkout_view, name='checkout'),
]



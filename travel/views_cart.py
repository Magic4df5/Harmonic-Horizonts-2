# travel/views.py (добавьте эти функции)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Ticket, Tour


def _get_or_create_cart(request):
    """Получить или создать корзину для пользователя"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True,
            defaults={'session_key': None}
        )
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            is_active=True,
            defaults={'user': None}
        )
    return cart


def cart_view(request):
    """Просмотр корзины"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all().select_related('ticket', 'tour')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price() if cart else 0,
    }
    return render(request, 'travel/cart.html', context)


@require_POST
def add_ticket_to_cart(request, ticket_id):
    """Добавить билет в корзину (POST запрос)"""
    ticket = get_object_or_404(Ticket, id=ticket_id, is_available=True)
    cart = _get_or_create_cart(request)

    # Проверяем, есть ли уже этот билет в корзине
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        ticket=ticket,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество билета "{ticket}" увеличено!')
    else:
        messages.success(request, f'Билет "{ticket}" добавлен в корзину!')

    return redirect(request.META.get('HTTP_REFERER', 'cart_view'))


@require_POST
def add_tour_to_cart(request, tour_id):
    """Добавить тур в корзину (POST запрос)"""
    tour = get_object_or_404(Tour, id=tour_id, is_available=True)
    cart = _get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        tour=tour,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество тура "{tour.title}" увеличено!')
    else:
        messages.success(request, f'Тур "{tour.title}" добавлен в корзину!')

    return redirect(request.META.get('HTTP_REFERER', 'cart_view'))


def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = _get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        item_name = str(cart_item.ticket) if cart_item.ticket else cart_item.tour.title
        cart_item.delete()
        messages.success(request, f'Товар "{item_name}" удален из корзины!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Товар не найден в корзине!')

    return redirect('cart_view')


@require_POST
def update_cart_item(request, item_id):
    """Изменить количество товара"""
    cart = _get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено!')
        else:
            cart_item.delete()
            messages.success(request, 'Товар удален из корзины!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Товар не найден в корзине!')

    return redirect('cart_view')


def clear_cart(request):
    """Очистить всю корзину"""
    cart = _get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Корзина очищена!')
    return redirect('cart_view')


def checkout_view(request):
    """Имитация оформления заказа"""
    cart = _get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста!')
        return redirect('cart_view')

    # Имитация оформления заказа
    messages.success(request, 'Заказ успешно оформлен!')

    # Очищаем корзину после "оформления"
    cart.items.all().delete()

    return render(request, 'travel/checkout.html', {'cart': cart})
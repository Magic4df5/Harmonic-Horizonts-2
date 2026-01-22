# travel/context_processors.py
from .models import Cart


def cart_context(request):
    """Добавляет корзину в контекст всех шаблонов"""
    cart = None
    cart_items_count = 0
    cart_total = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
        except Cart.DoesNotExist:
            cart = None
    else:
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key, is_active=True)
            except Cart.DoesNotExist:
                cart = None

    if cart:
        cart_items_count = cart.items.count()
        cart_total = cart.total_price()

    return {
        'cart': cart,
        'cart_items_count': cart_items_count,
        'cart_total': cart_total,
    }
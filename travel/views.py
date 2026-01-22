# travel/views.py - ПОЛНЫЙ ФАЙЛ
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import (
    Country, Tour, Review, Ticket, TicketOrder,
    EarlyBooking, Visa, News, Contact,
    Cart, CartItem
)


# ============ ХЕЛПЕР-ФУНКЦИИ ============

def get_or_create_cart(request):
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


# ============ АУТЕНТИФИКАЦИЯ ============

def login_view(request):
    """Страница входа - ВЕРСИЯ С ПОЛНОЙ ОТЛАДКОЙ"""
    print("\n" + "=" * 80)
    print("🔄 ФУНКЦИЯ login_view ВЫЗВАНА")
    print(f"📋 Метод запроса: {request.method}")
    print(f"👤 Пользователь аутентифицирован: {request.user.is_authenticated}")
    print(f"👤 Имя пользователя: {request.user}")

    if request.user.is_authenticated:
        print("✅ Пользователь уже вошел, редирект на главную")
        messages.info(request, 'Вы уже вошли в систему')
        return redirect('home')

    if request.method == 'POST':
        print("\n📨 ПОЛУЧЕН POST ЗАПРОС ДЛЯ ВХОДА")
        print(f"📊 Данные формы:")
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                print(f"   {key}: {value}")

        # Получаем данные
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        print(f"\n🔍 Проверяем данные:")
        print(f"   Имя пользователя: '{username}'")
        print(f"   Пароль: {'*' * len(password)} (длина: {len(password)})")

        # Валидация
        errors = []

        if not username:
            errors.append('Введите имя пользователя')
            print("   ❌ Ошибка: имя пользователя пустое")

        if not password:
            errors.append('Введите пароль')
            print("   ❌ Ошибка: пароль пустой")

        if errors:
            for error in errors:
                messages.error(request, error)
            print(f"   ⚠️ Всего ошибок: {len(errors)}")
        else:
            print("   ✅ Данные валидны, пытаемся аутентифицировать...")

            try:
                from django.contrib.auth import authenticate, login

                print(f"\n🔐 Аутентифицируем пользователя '{username}'...")
                user = authenticate(username=username, password=password)

                if user is not None:
                    print(f"   ✅ Пользователь найден: {user.username} (ID: {user.id})")
                    print(f"   ✅ Пользователь активен: {user.is_active}")

                    # Логиним
                    login(request, user)
                    print(f"   ✅ Пользователь вошел: {request.user.username}")
                    print(f"   ✅ Аутентифицирован: {request.user.is_authenticated}")

                    messages.success(request, f'👋 Добро пожаловать, {user.username}!')

                    print("\n🔄 Редирект на главную...")
                    # Явно проверяем редирект
                    response = redirect('home')
                    print(f"   ✅ Редирект создан: {response.url}")
                    return response
                else:
                    print(f"   ❌ Аутентификация не удалась")
                    print(f"   ❌ Проверьте: существует ли пользователь '{username}'?")
                    print(f"   ❌ Правильный ли пароль?")

                    # Проверяем существует ли пользователь
                    from django.contrib.auth.models import User
                    if User.objects.filter(username=username).exists():
                        print(f"   ℹ️ Пользователь '{username}' существует в базе")
                        messages.error(request, '❌ Неверный пароль')
                    else:
                        print(f"   ℹ️ Пользователь '{username}' НЕ существует в базе")
                        messages.error(request, '❌ Пользователь не найден')

            except Exception as e:
                print(f"\n💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Ошибка сервера: {str(e)}')

    else:
        print("📄 GET запрос - показываем форму входа")

    print("\n🖥️ Рендерим шаблон login.html...")
    # Если GET запрос или ошибка в POST
    return render(request, 'travel/login.html', {
        'title': 'Вход в систему'
    })


def register_view(request):
    """Страница регистрации - ВЕРСИЯ С ПОЛНОЙ ОТЛАДКОЙ"""
    print("\n" + "=" * 80)
    print("🔄 ФУНКЦИЯ register_view ВЫЗВАНА")
    print(f"📋 Метод запроса: {request.method}")
    print(f"👤 Пользователь аутентифицирован: {request.user.is_authenticated}")
    print(f"👤 Имя пользователя: {request.user}")

    if request.user.is_authenticated:
        print("✅ Пользователь уже вошел, редирект на главную")
        return redirect('home')

    if request.method == 'POST':
        print("\n📨 ПОЛУЧЕН POST ЗАПРОС")
        print(f"📊 Данные формы:")
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                print(f"   {key}: {value}")

        # Получаем данные
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        print(f"\n🔍 Проверяем данные:")
        print(f"   Имя пользователя: '{username}' (длина: {len(username)})")
        print(f"   Email: '{email}'")
        print(f"   Пароль 1: {'*' * len(password1)} (длина: {len(password1)})")
        print(f"   Пароль 2: {'*' * len(password2)} (длина: {len(password2)})")

        # Валидация
        errors = []

        if not username:
            errors.append('Введите имя пользователя')
            print("   ❌ Ошибка: имя пользователя пустое")

        if not email:
            errors.append('Введите email')
            print("   ❌ Ошибка: email пустой")

        if not password1:
            errors.append('Введите пароль')
            print("   ❌ Ошибка: пароль пустой")

        if password1 != password2:
            errors.append('Пароли не совпадают')
            print("   ❌ Ошибка: пароли не совпадают")

        if errors:
            for error in errors:
                messages.error(request, error)
            print(f"   ⚠️ Всего ошибок: {len(errors)}")
        else:
            print("   ✅ Данные валидны")

            try:
                from django.contrib.auth.models import User
                from django.contrib.auth import login

                print("\n👤 Создаем пользователя...")

                # Проверяем, не существует ли уже такой пользователь
                if User.objects.filter(username=username).exists():
                    print(f"   ❌ Пользователь с именем '{username}' уже существует!")
                    messages.error(request, 'Пользователь с таким именем уже существует')
                elif User.objects.filter(email=email).exists():
                    print(f"   ❌ Пользователь с email '{email}' уже существует!")
                    messages.error(request, 'Пользователь с таким email уже существует')
                else:
                    # Создаем пользователя
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1
                    )
                    print(f"   ✅ Пользователь создан: {user.username} (ID: {user.id})")

                    print("\n🔐 Логиним пользователя...")
                    # Логиним
                    login(request, user)
                    print(f"   ✅ Пользователь вошел: {request.user.username}")
                    print(f"   ✅ Аутентифицирован: {request.user.is_authenticated}")

                    messages.success(request, f'🎉 Добро пожаловать, {username}!')

                    print("\n🔄 Редирект на главную...")
                    # Явно проверяем редирект
                    response = redirect('home')
                    print(f"   ✅ Редирект создан: {response.url}")
                    return response

            except Exception as e:
                print(f"\n💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Ошибка сервера: {str(e)}')

    else:
        print("📄 GET запрос - показываем форму регистрации")

    print("\n🖥️ Рендерим шаблон register.html...")
    # Если GET запрос или ошибка в POST
    return render(request, 'travel/register.html')



def logout_view(request):
    """Выход из системы"""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, '👋 Вы успешно вышли из системы.')
    return redirect('home')


def check_auth(request):
    """Проверка авторизации для AJAX"""
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })


# ============ ОСНОВНЫЕ СТРАНИЦЫ (CBV) ============

class HomeView(TemplateView):
    template_name = 'travel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.filter(is_published=True)[:3]
        context['tours'] = Tour.objects.filter(is_available=True)[:6]
        context['tickets'] = Ticket.objects.filter(is_available=True)[:6]
        return context


class CountryListView(ListView):
    model = Country
    template_name = 'travel/countries.html'
    context_object_name = 'countries'


class TourListView(ListView):
    model = Tour
    template_name = 'travel/tours.html'
    context_object_name = 'tours'
    paginate_by = 9

    def get_queryset(self):
        return Tour.objects.filter(is_available=True)


class TourDetailView(DetailView):
    model = Tour
    template_name = 'travel/tour_detail.html'
    context_object_name = 'tour'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(
            tour=self.object,
            is_published=True
        )
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class ReviewListView(ListView):
    model = Review
    template_name = 'travel/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(is_published=True)


class ContactView(TemplateView):
    template_name = 'travel/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        return context


class VisaView(ListView):
    model = Visa
    template_name = 'travel/visas.html'
    context_object_name = 'visas'

    def get_queryset(self):
        return Visa.objects.filter(is_available=True)


# ============ БИЛЕТЫ ============

class TicketListView(ListView):
    model = Ticket
    template_name = 'travel/tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        ticket_type = self.kwargs.get('type')
        queryset = Ticket.objects.filter(is_available=True)

        if ticket_type == 'train':
            queryset = queryset.filter(type='train')
        elif ticket_type == 'air':
            queryset = queryset.filter(type='air')

        return queryset.order_by('departure_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_type'] = self.kwargs.get('type', 'all')
        context['title'] = 'ЖД билеты' if context['ticket_type'] == 'train' else 'Авиабилеты'
        return context


@login_required
def book_ticket(request, ticket_id):
    """Оформление билета"""
    ticket = get_object_or_404(Ticket, id=ticket_id, is_available=True)

    if request.method == 'POST':
        # Создаем заказ
        TicketOrder.objects.create(
            ticket=ticket,
            user=request.user,
            passenger_name=request.POST.get('passenger_name'),
            passenger_email=request.POST.get('passenger_email'),
            passenger_phone=request.POST.get('passenger_phone')
        )

        # Уменьшаем количество доступных мест
        ticket.available_seats -= 1
        if ticket.available_seats <= 0:
            ticket.is_available = False
        ticket.save()

        messages.success(request, 'Билет успешно оформлен! Проверьте вашу почту.')
        return redirect('tickets', type=ticket.type)

    return render(request, 'travel/book_ticket.html', {
        'ticket': ticket,
        'title': f'Оформление билета'
    })


@login_required
def my_tickets(request):
    """Мои билеты"""
    orders = TicketOrder.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'travel/my_tickets.html', {
        'orders': orders,
        'title': 'Мои билеты'
    })


# ============ КОРЗИНА ============

@require_POST
def add_to_cart(request, item_id):
    """Добавить товар в корзину (билет или тур)"""
    item_type = request.POST.get('item_type', 'ticket')

    # Получаем товар
    if item_type == 'ticket':
        item = get_object_or_404(Ticket, id=item_id, is_available=True)
        item_name = str(item)
    else:  # tour
        item = get_object_or_404(Tour, id=item_id, is_available=True)
        item_name = item.title

    # Получаем или создаем корзину
    cart = get_or_create_cart(request)

    # Добавляем товар в корзину
    if item_type == 'ticket':
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            ticket=item,
            defaults={'quantity': 1}
        )
    else:  # tour
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            tour=item,
            defaults={'quantity': 1}
        )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        message = f'✅ Добавлен еще один "{item_name}"'
    else:
        message = f'✅ "{item_name}" добавлен в корзину'

    # Ответ для AJAX или обычный редирект
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.items_count(),
            'item_type': item_type
        })

    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'cart_view'))


def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        item_name = str(cart_item.ticket) if cart_item.ticket else cart_item.tour.title
        cart_item.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'✅ "{item_name}" удален из корзины',
                'cart_count': cart.items_count(),
                'total_price': cart.total_price()
            })

        messages.success(request, f'✅ "{item_name}" удален из корзины')
        return redirect('cart_view')

    except CartItem.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Товар не найден'})
        messages.error(request, '❌ Товар не найден в корзине')
        return redirect('cart_view')


def cart_view(request):
    """Просмотр корзины"""
    cart = get_or_create_cart(request)
    items = cart.items.all().select_related('ticket', 'tour')

    return render(request, 'travel/cart.html', {
        'cart': cart,
        'items': items,
        'total_price': cart.total_price(),
        'title': 'Корзина'
    })


@require_POST
def update_cart_item(request, item_id):
    """Обновить количество товара в корзине"""
    cart = get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            message = '✅ Количество обновлено'
        else:
            item_name = str(cart_item.ticket) if cart_item.ticket else cart_item.tour.title
            cart_item.delete()
            message = f'✅ "{item_name}" удален из корзины'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_count': cart.items_count(),
                'total_price': cart.total_price(),
                'item_total': cart_item.total_price() if quantity > 0 else 0
            })

        messages.success(request, message)
        return redirect('cart_view')

    except (CartItem.DoesNotExist, ValueError) as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        messages.error(request, '❌ Ошибка обновления корзины')
        return redirect('cart_view')


def clear_cart(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)

    if cart:
        items_count = cart.items_count()
        cart.items.all().delete()
        cart.delete()
        messages.success(request, f'✅ Корзина очищена (удалено {items_count} товаров)')

    return redirect('cart_view')


def checkout_view(request):
    """Оформление заказа (имитация)"""
    cart = get_or_create_cart(request)

    if not cart or not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста!')
        return redirect('cart_view')

    total_price = cart.total_price()
    items_count = cart.items_count()

    # Имитация оформления заказа
    messages.success(request, f'🎉 Заказ на сумму {total_price} руб. успешно оформлен! Это имитация покупки.')

    # Очищаем корзину
    cart.items.all().delete()
    cart.delete()

    return render(request, 'travel/checkout.html', {
        'total_price': total_price,
        'items_count': items_count,
        'title': 'Заказ оформлен'
    })


# ============ ОТЗЫВЫ ============

@require_POST
def add_review(request):
    """Добавление отзыва"""
    if not request.user.is_authenticated:
        messages.error(request, 'Для добавления отзыва необходимо войти в систему')
        return redirect('login')

    tour_id = request.POST.get('tour')
    text = request.POST.get('text')
    rating = request.POST.get('rating')

    if tour_id and text and rating:
        try:
            tour = Tour.objects.get(id=tour_id)
            Review.objects.create(
                author=request.user.username,
                tour=tour,
                text=text,
                rating=int(rating),
                is_published=True
            )
            messages.success(request, '✅ Ваш отзыв успешно добавлен!')
        except Tour.DoesNotExist:
            messages.error(request, '❌ Тур не найден')
        except ValueError:
            messages.error(request, '❌ Некорректный рейтинг')

    return redirect('reviews')
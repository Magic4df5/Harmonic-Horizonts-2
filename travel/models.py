# travel/models.py - ИСПРАВЛЕННЫЙ ФАЙЛ
from django.db import models
from django.conf import settings
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название страны')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='countries/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Tour(models.Model):
    TOUR_TYPES = [
        ('beach', 'Пляжный отдых'),
        ('excursion', 'Экскурсионный'),
        ('ski', 'Горнолыжный'),
        ('cruise', 'Круиз'),
        ('safari', 'Сафари'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название тура')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    description = models.TextField(verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Длительность (дней)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES, verbose_name='Тип тура')
    image = models.ImageField(upload_to='tours/', verbose_name='Изображение')
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    author = models.CharField(max_length=100, verbose_name='Автор')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.author}'


# ПЕРЕМЕСТИТЕ TicketType выше, чтобы использовать в моделях
class TicketType(models.TextChoices):
    TRAIN = 'train', 'ЖД билет'
    AIR = 'air', 'Авиабилет'


class Ticket(models.Model):
    type = models.CharField(max_length=20, choices=TicketType.choices, verbose_name='Тип билета')
    departure_city = models.CharField(max_length=100, verbose_name='Город отправления')
    arrival_city = models.CharField(max_length=100, verbose_name='Город прибытия')
    departure_date = models.DateTimeField(verbose_name='Дата отправления')
    arrival_date = models.DateTimeField(verbose_name='Дата прибытия')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available_seats = models.IntegerField(default=50, verbose_name='Доступные места')
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ['departure_date']

    def __str__(self):
        return f'{self.get_type_display()} {self.departure_city} → {self.arrival_city}'


class TicketBooking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Билет')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    passenger_name = models.CharField(max_length=100, verbose_name='Имя пассажира')
    passenger_email = models.EmailField(verbose_name='Email пассажира')
    passenger_phone = models.CharField(max_length=20, verbose_name='Телефон пассажира')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтвержден')

    class Meta:
        verbose_name = 'Бронирование билета'
        verbose_name_plural = 'Бронирования билетов'

    def __str__(self):
        return f'Бронирование {self.id} для {self.passenger_name}'


class EarlyBooking(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    booking_date = models.DateField(verbose_name='Дата бронирования')
    comments = models.TextField(blank=True, verbose_name='Комментарии')
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    class Meta:
        verbose_name = 'Раннее бронирование'
        verbose_name_plural = 'Ранние бронирования'

    def __str__(self):
        return f'Бронирование от {self.name}'


class Visa(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    requirements = models.TextField(verbose_name='Требования')
    processing_time = models.CharField(max_length=50, verbose_name='Срок оформления')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    is_available = models.BooleanField(default=True, verbose_name='Доступно')

    class Meta:
        verbose_name = 'Виза'
        verbose_name_plural = 'Визы'

    def __str__(self):
        return f'Виза в {self.country.name}'


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Contact(models.Model):
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    work_hours = models.CharField(max_length=100, verbose_name='Часы работы')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return 'Контактная информация'


class TicketOrder(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Билет')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    passenger_name = models.CharField(max_length=100, verbose_name='Имя пассажира')
    passenger_email = models.EmailField(verbose_name='Email пассажира')
    passenger_phone = models.CharField(max_length=20, verbose_name='Телефон пассажира')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтвержден')

    class Meta:
        verbose_name = 'Заказ билета'
        verbose_name_plural = 'Заказы билетов'

    def __str__(self):
        return f'Заказ {self.id} на {self.ticket}'


# ============================================================
# МОДЕЛИ КОРЗИНЫ - ТОЛЬКО ОДИН РАЗ, ПРАВИЛЬНЫЕ ОТСТУПЫ
# ============================================================

class Cart(models.Model):
    """Корзина пользователя - для имитации покупок"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)  # для неавторизованных пользователей
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username}"
        return f"Корзина (сессия: {self.session_key})"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def items_count(self):
        return self.items.count()


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, null=True, blank=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True, blank=True)  # для туров
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'ticket']  # чтобы один товар не добавлялся дважды

    def __str__(self):
        if self.ticket:
            return f"{self.ticket} x{self.quantity}"
        return f"{self.tour} x{self.quantity}"

    def total_price(self):
        if self.ticket:
            return self.ticket.price * self.quantity
        elif self.tour:
            return self.tour.price * self.quantity
        return 0
# travel/forms.py (создайте новый файл)
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import TicketOrder, Review


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru',
            'style': 'padding: 12px; border-radius: 10px; border: 2px solid var(--mlp-purple);'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте логин',
            'style': 'padding: 12px; border-radius: 10px; border: 2px solid var(--mlp-purple);'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте пароль',
            'style': 'padding: 12px; border-radius: 10px; border: 2px solid var(--mlp-purple);'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'style': 'padding: 12px; border-radius: 10px; border: 2px solid var(--mlp-purple);'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин',
            'style': 'padding: 12px; border-radius: 10px; border: 2px solid var(--mlp-purple);'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'style': 'padding: 12px; border-radius: 10px; border: 2px solid var(--mlp-purple);'
        })
    )


class TicketOrderForm(forms.ModelForm):
    class Meta:
        model = TicketOrder
        fields = ['passenger_name', 'passenger_email', 'passenger_phone']
        widgets = {
            'passenger_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя Фамилия'
            }),
            'passenger_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'passenger_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'text', 'rating', 'tour']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв...',
                'rows': 4
            }),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'tour': forms.HiddenInput()
        }
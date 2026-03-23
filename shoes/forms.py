from django import forms
from django.core.exceptions import ValidationError

from .models import STATUS_CHOICES, Order, PickupPoint, Product, User


class ProductForm(forms.ModelForm):
    """Форма для создания/редактирования товара."""
    class Meta:
        model = Product
        fields = [
            'article',
            'name',
            'category',
            'manufacturer',
            'supplier',
            'unit',
            'price',
            'discount',
            'quantity',
            'description',
            'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'discount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'quantity': forms.NumberInput(attrs={'min': '0'}),
        }
        help_texts = {
            'discount': 'Скидка в процентах (0-100)',
            'image': 'Рекомендуемый размер 300x200 пикселей',
        }

    def clean_price(self):
        """Цена не может быть отрицательной."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_quantity(self):
        """Количество не может быть отрицательным."""
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise ValidationError('Количество не может быть отрицательным.')
        return quantity

    def clean_discount(self):
        """Скидка должна быть от 0 до 100%."""
        discount = self.cleaned_data.get('discount')
        if discount is not None and (discount < 0 or discount > 100):
            raise ValidationError('Скидка должна быть в пределах от 0 до 100%.')
        return discount


class OrderForm(forms.ModelForm):
    """Форма для создания/редактирования заказа."""
    class Meta:
        model = Order
        fields = [
            'order_number',
            'order_date',
            'delivery_date',
            'pickup_point',
            'client',
            'pickup_code',
            'status',
        ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=STATUS_CHOICES),
        }
        help_texts = {
            'order_number': 'Только цифры',
            'pickup_code': 'Только цифры',
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы заказа."""
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор активными пользователями и существующими пунктами выдачи
        self.fields['client'].queryset = User.objects.filter(is_active=True)
        self.fields['pickup_point'].queryset = PickupPoint.objects.all()

    def clean_order_number(self):
        """Номер заказа должен содержать только цифры."""
        order_number = self.cleaned_data.get('order_number')
        if order_number and not order_number.isdigit():
            raise ValidationError('Номер заказа должен содержать только цифры.')
        return order_number

    def clean_pickup_code(self):
        """Код получения должен содержать только цифры."""
        pickup_code = self.cleaned_data.get('pickup_code')
        if pickup_code and not pickup_code.isdigit():
            raise ValidationError('Код получения должен содержать только цифры.')
        return pickup_code

    def clean(self):
        """Дата доставки не может быть раньше даты заказа."""
        cleaned_data = super().clean()
        order_date = cleaned_data.get('order_date')
        delivery_date = cleaned_data.get('delivery_date')
        if order_date and delivery_date and delivery_date < order_date:
            self.add_error(
                'delivery_date',
                'Дата доставки не может быть раньше даты заказа.'
            )
        return cleaned_data
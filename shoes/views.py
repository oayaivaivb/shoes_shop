import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from PIL import Image

from .forms import OrderForm, ProductForm
from .models import Order, Product, Supplier


def resize_product_image(product):
    """Уменьшает изображение товара до 300×200 пикселей."""
    if product.image and os.path.exists(product.image.path):
        img = Image.open(product.image.path)
        img.thumbnail((300, 200), Image.Resampling.LANCZOS)
        img.save(product.image.path)


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Доступ только для пользователей с ролью 'admin'."""
    def test_func(self):
        return (self.request.user.is_authenticated
                and self.request.user.profile.role == 'admin')


class ManagerOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Доступ для пользователей с ролью 'manager' или 'admin'."""
    def test_func(self):
        return (self.request.user.is_authenticated 
                and self.request.user.profile.role in ('admin', 'manager'))


class ProductListView(ListView):
    model = Product
    template_name = 'shoes/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'category', 'manufacturer', 'supplier', 'unit'
        )

        # Поиск по нескольким текстовым полям
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q)
                | Q(description__icontains=q)
                | Q(manufacturer__name__icontains=q)
                | Q(supplier__name__icontains=q)
                | Q(category__name__icontains=q)
            )

        # Фильтр по поставщику
        supplier_id = self.request.GET.get('supplier')
        if supplier_id and supplier_id != 'all':
            queryset = queryset.filter(supplier_id=supplier_id)

        # Сортировка по количеству на складе
        sort = self.request.GET.get('sort')
        if sort == 'quantity':
            queryset = queryset.order_by('quantity')
        elif sort == '-quantity':
            queryset = queryset.order_by('-quantity')
        else:
            queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        context['current_q'] = self.request.GET.get('q', '')
        context['current_supplier'] = self.request.GET.get('supplier', 'all')
        context['current_sort'] = self.request.GET.get('sort', '')

        # Вычисляем цену со скидкой для каждого товара
        for product in context['products']:
            product.final_price = product.price * (100 - product.discount) / 100
        return context


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shoes/product_form.html'
    success_url = reverse_lazy('shoes:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно добавлен.')
        resize_product_image(self.object)
        return response


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shoes/product_form.html'
    success_url = reverse_lazy('shoes:product_list')

    def form_valid(self, form):
        old_image = self.get_object().image
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно обновлён.')
        new_image = self.object.image
        if (
            old_image
            and old_image != new_image
            and os.path.exists(old_image.path)
        ):
            os.remove(old_image.path)
        resize_product_image(self.object)
        return response


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'shoes/product_confirm_delete.html'
    success_url = reverse_lazy('shoes:product_list')

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        # Запрет удаления, если товар есть в заказах
        if product.order_items.exists():
            messages.error(
                request, 'Нельзя удалить товар, который есть в заказах.')
            return redirect('shoes:product_list')
        if product.image and os.path.exists(product.image.path):
            os.remove(product.image.path)
        messages.success(request, 'Товар удалён.')
        return super().post(request, *args, **kwargs)


class OrderListView(ManagerOrAdminRequiredMixin, ListView):
    model = Order
    template_name = 'shoes/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'pickup_point', 'client__profile'
        ).order_by('-order_date')


class OrderCreateView(AdminRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shoes/order_form.html'
    success_url = reverse_lazy('shoes:order_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Заказ №{self.object.order_number} успешно создан.'
        )
        return response


class OrderUpdateView(AdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shoes/order_form.html'
    success_url = reverse_lazy('shoes:order_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Заказ №{self.object.order_number} успешно обновлён.'
        )
        return response


class OrderDeleteView(AdminRequiredMixin, DeleteView):
    model = Order
    template_name = 'shoes/order_confirm_delete.html'
    success_url = reverse_lazy('shoes:order_list')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        # Сообщение добавляем до вызова super().post(), чтобы оно сохранилось
        messages.success(
            request,
            f'Заказ №{order.order_number} успешно удалён.'
        )
        return super().post(request, *args, **kwargs)
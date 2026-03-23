from django.contrib import admin

from .models import (Category, Manufacturer, Order, OrderItem, PickupPoint,
                     Product, Profile, Supplier, Unit)


class OrderItemInline(admin.TabularInline):
    """Inline-редактирование позиций заказа прямо на странице заказа."""
    model = OrderItem
    extra = 1
    raw_id_fields = ('product',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Администрирование профилей пользователей."""
    list_display = ('user', 'full_name', 'role')
    list_filter = ('role',)
    search_fields = ('full_name', 'user__username', 'user__email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Администрирование категорий товаров."""
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """Администрирование производителей."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Администрирование поставщиков."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Администрирование единиц измерения."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Администрирование товаров."""
    list_display = ('article', 'name', 'category', 'manufacturer', 'supplier',
                    'price', 'discount', 'quantity', 'unit')
    list_filter = ('category', 'manufacturer', 'supplier', 'unit')
    search_fields = ('article', 'name', 'description')
    raw_id_fields = ('category', 'manufacturer', 'supplier', 'unit')
    fieldsets = (
        (None, {
            'fields': ('article', 'name', 'category', 'manufacturer',
                       'supplier', 'unit', 'price', 'discount', 'quantity')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
    )


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    """Администрирование пунктов выдачи."""
    list_display = ('address',)
    search_fields = ('address',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Администрирование заказов."""
    list_display = ('order_number', 'order_date', 'delivery_date', 'pickup_point',
                    'client', 'status', 'pickup_code')
    list_filter = ('status', 'order_date', 'pickup_point')
    search_fields = ('order_number', 'client__username', 'client__email')
    raw_id_fields = ('client', 'pickup_point')
    date_hierarchy = 'order_date'
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Администрирование позиций заказов."""
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('order__order_number', 'product__name', 'product__article')
    raw_id_fields = ('order', 'product')
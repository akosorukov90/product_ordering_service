from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, CustomUser, Contact, OrderItem, Order


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'type', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active', 'type')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'company', 'position', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'company', 'position', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

# class ShopCategoryInline(admin.TabularInline):
#     model = Category.shops.through
#     extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass
    # inlines = [ShopCategoryInline]


@admin.register(Category)
class ShopAdmin(admin.ModelAdmin):
    pass
    # inlines = [ShopCategoryInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

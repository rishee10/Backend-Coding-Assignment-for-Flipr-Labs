from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Cart, CartItem, Order, CustomUser

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  # Added 'quantity' since it's part of CartItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'shipping_address')  # Ensure these fields exist in the Order model

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')  # Ensure 'user' field exists in the Cart model

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'category')  # Added 'category' for completeness

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_superuser')  # Added fields for CustomUser

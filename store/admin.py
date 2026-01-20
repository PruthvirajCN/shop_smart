from .models import Review
from .models import Coupon
from .models import Wishlist
from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "id")

admin.site.register(Order, OrderAdmin)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Coupon)
from .models import Review
admin.site.register(Review)

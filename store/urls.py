from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),

    # ✅ CART
path("cart/", views.cart_view, name="cart"),
path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
path("cart/remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),
path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
path("cart/remove-coupon/", views.remove_coupon, name="remove_coupon"),

    path("checkout/", views.checkout_view, name="checkout"),
    path("my-orders/", views.my_orders, name="my_orders"),

    # ✅ AUTH
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ✅ WISHLIST
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:item_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("product/<int:product_id>/review/", views.add_review, name="add_review"),

]


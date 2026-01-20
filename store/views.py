from django.core.paginator import Paginator
from .models import Review
from .models import Coupon
from .models import Wishlist
from decimal import Decimal
from .models import Order, OrderItem
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, CartItem


# ✅ HOME PAGE
def home(request):
    featured_products = Product.objects.all()[:8]
    categories = Category.objects.all()

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list("product_id", flat=True))

    return render(request, "store/home.html", {
        "featured_products": featured_products,
        "categories": categories,
        "wishlist_ids": wishlist_ids
    })

# ✅ PRODUCTS LIST PAGE
def products(request):
    q = request.GET.get("q")
    category_id = request.GET.get("category")
    sort = request.GET.get("sort")

    product_list = Product.objects.all()
    categories = Category.objects.all()

    # ✅ Search
    if q:
        product_list = product_list.filter(name__icontains=q)

    # ✅ Category Filter
    if category_id:
        product_list = product_list.filter(category__id=category_id)

    # ✅ Sorting
    if sort == "new":
        product_list = product_list.order_by("-id")
    elif sort == "price_low":
        product_list = product_list.order_by("price")
    elif sort == "price_high":
        product_list = product_list.order_by("-price")
    elif sort == "az":
        product_list = product_list.order_by("name")
    elif sort == "za":
        product_list = product_list.order_by("-name")
    else:
        product_list = product_list.order_by("-id")

    # ✅ Pagination (8 products per page)
    paginator = Paginator(product_list, 8)
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    # ✅ Wishlist ids
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(user=request.user)
            .values_list("product_id", flat=True)
        )

    return render(request, "store/products.html", {
        "products": products_page,
        "categories": categories,
        "wishlist_ids": wishlist_ids
    })



# ✅ PRODUCT DETAILS PAGE
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]

    reviews = Review.objects.filter(product=product).order_by("-id")

    # ✅ Average Rating
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
    else:
        avg_rating = 0

    return render(request, "store/product_detail.html", {
        "product": product,
        "related_products": related_products,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
    })
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect("product_detail", id=product.id)



# ✅ ADD TO CART
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


# ✅ VIEW CART
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    subtotal = sum(item.product.price * item.quantity for item in items)
    tax = subtotal * Decimal("0.05")

    discount = Decimal("0.00")
    coupon_message = ""
    applied_code = request.session.get("coupon_code")

    # ✅ Apply coupon if already saved in session
    if applied_code:
        try:
            coupon = Coupon.objects.get(code=applied_code, active=True)
            if coupon.discount_type == "percent":
                discount = (subtotal * coupon.discount_value) / Decimal("100")
            else:
                discount = coupon.discount_value

            # Prevent negative discount
            if discount > subtotal:
                discount = subtotal

        except Coupon.DoesNotExist:
            request.session.pop("coupon_code", None)

    # ✅ Apply coupon when submitted
    if request.method == "POST":
        code = request.POST.get("coupon", "").strip().upper()

        try:
            coupon = Coupon.objects.get(code=code, active=True)
            request.session["coupon_code"] = code
            coupon_message = f"✅ Coupon '{code}' applied!"

            if coupon.discount_type == "percent":
                discount = (subtotal * coupon.discount_value) / Decimal("100")
            else:
                discount = coupon.discount_value

            if discount > subtotal:
                discount = subtotal

        except Coupon.DoesNotExist:
            request.session.pop("coupon_code", None)
            coupon_message = "❌ Invalid coupon code!"

    total = subtotal + tax - discount

    return render(request, "store/cart.html", {
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total,
        "coupon_message": coupon_message,
        "applied_code": applied_code
    })



# ✅ REMOVE CART ITEM
@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("cart")


# ✅ UPDATE CART ITEM QUANTITY
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        qty = int(request.POST.get("quantity"))
        if qty > 0:
            cart_item.quantity = qty
            cart_item.save()

    return redirect("cart")
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("home")

    return render(request, "store/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "store/login.html", {"error": "Invalid credentials"})

    return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")
@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        return redirect("products")

    subtotal = sum(item.product.price * item.quantity for item in items)
    tax = subtotal * Decimal("0.05")
    total = subtotal + tax


    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        # ✅ Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=total,
            status="Placed"
        )

        # ✅ Create Order Items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # ✅ Clear Cart after order
        items.delete()

        return redirect("my_orders")

    return render(request, "store/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "store/my_orders.html", {"orders": orders})
@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    if not items:
        return redirect("products")

    subtotal = sum(item.product.price * item.quantity for item in items)
    tax = subtotal * Decimal("0.05")
    total = subtotal + tax


    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=total,
            status="Placed"
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        items.delete()
        return redirect("my_orders")

    return render(request, "store/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    })


@login_required
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id").prefetch_related("items__product")
    return render(request, "store/my_orders.html", {"orders": orders})

def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by("-id")
    return render(request, "store/wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect("wishlist")


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    return redirect("wishlist")
@login_required
def remove_coupon(request):
    request.session.pop("coupon_code", None)
    return redirect("cart")

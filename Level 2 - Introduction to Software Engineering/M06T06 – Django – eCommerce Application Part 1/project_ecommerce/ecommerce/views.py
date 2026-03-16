from datetime import datetime
import hashlib
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Purchase, Review, Store
from .models import ResetToken
from .forgot_password import (
    build_email,
    generate_reset_url,
    change_user_password,
)


def product_list(request):
    '''
    View to display a list of all products available in the database.
    '''
    products = Product.objects.select_related("store").all()

    return render(
        request, "ecommerce/product_list.html", {"products": products}
    )


def login_user(request):
    '''
    Handles user login using username and password. If successful, the user is
    redirected to the product list page. If the credentials are incorrect, an
    error is displayed.
    '''
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("product_list")
        else:
            return render(
                request,
                "ecommerce/login.html",
                {"error": "Invalid credentials"},
            )

    return render(request, "ecommerce/login.html")


def logout_user(request):
    '''
    Logs out the current user and redirects to the login page.
    '''
    if request.user is not None:
        logout(request)
        return HttpResponseRedirect(reverse("ecommerce:login"))


def register(request):
    '''
    Handles user registration. It creates a new user from the provided
    username, password, email, and account type (vendor or buyer).
    '''
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        account_type = request.POST.get("account_type")

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        group = Group.objects.get(name=account_type)
        user.groups.add(group)

        if account_type == "vendor":
            Store.objects.create(vendor=user, name=f"{user.username}'s Shop")

        user.save()
        login(request, user)

        return redirect("product_list")

    return render(request, "ecommerce/register.html")


@login_required
def vendor_hub(request):
    '''Shows the vendor's dashboard with their stores and products.'''
    my_stores = Store.objects.filter(vendor=request.user)
    return render(
        request, "ecommerce/vendor_hub.html", {"my_stores": my_stores}
    )


@login_required
def create_stores(request):
    '''Creates a new store for the vendor.'''
    if request.method == "POST":
        name = request.POST.get("store_name")
        if name:
            Store.objects.create(vendor=request.user, name=name)
    return redirect("vendor_hub")


@login_required
def add_products(request):
    '''Adds a new product to a specific store owned by the vendor.'''
    if request.method == "POST":
        store_id = request.POST.get("store_id")

        Product.objects.create(
            store=Store.objects.get(id=store_id),
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
        )
    return redirect("vendor_hub")


@login_required
def view_stores(request, store_id):
    '''Displays products for a specific store owned by the vendor.'''
    store = Store.objects.get(id=store_id, vendor=request.user)
    products = Product.objects.filter(store=store)

    return render(
        request,
        "ecommerce/store_detail.html",
        {"store": store, "products": products},
    )


@login_required
def change_stores(request, store_id):
    '''Allows the vendor to edit the name of one of their selected stores.'''
    store = Store.objects.get(id=store_id, vendor=request.user)

    if request.method == "POST":
        store.name = request.POST.get("store_name")
        store.save()
        return redirect("store_detail", store_id=store.id)

    return render(request, "ecommerce/edit_store.html", {"store": store})


@login_required
def delete_stores(request, store_id):
    '''Allows the vendor to delete one of their selected stores and all
      products in that store.'''
    store = Store.objects.get(id=store_id, vendor=request.user)
    store.delete()
    # Redirect back to the hub since the store is gone
    return redirect("vendor_hub")


@login_required
def delete_products(request, product_id):
    '''
    Allows the vendor to delete one of their products within a given store.
    '''
    product = Product.objects.get(id=product_id, store__vendor=request.user)
    store_id = product.store.id
    product.delete()
    return redirect("store_detail", store_id=store_id)


@login_required
def change_products(request, product_id):
    '''
    Allows the vendor to edit the details of one of their products
    within a given store.
    '''
    product = Product.objects.get(id=product_id, store__vendor=request.user)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()
        return redirect("store_detail", store_id=product.store.id)

    return render(request, "ecommerce/edit_product.html", {"product": product})


@login_required
def add_to_cart(request, product_id):
    '''
    Allows a buyer to add a product to their shopping cart, which is
    stored in the session.
    '''
    cart = request.session.get("cart", {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session["cart"] = cart
    return redirect("product_list")


@login_required
def view_cart(request):
    '''
    Displays the contents of the buyer's shopping cart, including product
    details and total cost.
    '''
    cart = request.session.get("cart", {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    # Calculate total for a simple checkout experience
    total = 0
    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append(
            {"product": product, "quantity": quantity, "subtotal": subtotal}
        )

    return render(
        request,
        "ecommerce/cart.html",
        {"cart_items": cart_items, "total": total},
    )


@login_required
def checkout(request):
    """
    Calculates the total cost of the items in the buyer's cart, ensures
    purchase object is created to save the purchase history, sends an invoice
    email to the buyer, and clears the cart."""
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("product_list")

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    total = 0
    items_list = ""

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.price * qty
        total += subtotal
        items_list += f"- {product.name} (x{qty}): ${subtotal}\n"

        product.stock -= qty
        product.save()
        Purchase.objects.get_or_create(user=request.user, product=product)

    subject = "Your Invoice from THE SHOP"
    message = f"Hi {request.user.username},\n\nOrder Summary:\n{items_list}\nTotal: ${total}\n\nThanks for shopping!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=True,
    )

    request.session["cart"] = {}
    return redirect("product_list")


def product_reviews(request, product_id):
    '''
    Displays reviews for a specific product and allows all users to
    submit a review. If a user has purchased the product, their review is
    seen as verified.
    '''
    product = Product.objects.get(id=product_id)
    reviews = Review.objects.filter(product=product)

    has_bought = False
    if request.user.is_authenticated:
        has_bought = Purchase.objects.filter(
            user=request.user, product=product
        ).exists()

    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content")
        if content:
            Review.objects.create(
                product=product,
                user=request.user,
                content=content,
                is_verified=has_bought,
            )
            return redirect("product_reviews", product_id=product.id)

    return render(
        request,
        "ecommerce/product_reviews.html",
        {"product": product, "reviews": reviews, "has_bought": has_bought},
    )


def send_password_reset(request):
    '''
    Handles the password reset request by generating a reset URL and sending a
    password reset email to the user. If email does not exist, it redirects to
    the login page without revealing that the email is not registered for
    security reasons.
    '''
    if request.method == "POST":
        user_email = request.POST.get("email")
        try:
            user = User.objects.get(email=user_email)
            url = generate_reset_url(user)
            email = build_email(user, url)
            email.send()
        except User.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse("login"))
    return render(request, "ecommerce/password_reset_request.html")


def reset_user_password(request, token):
    '''
    Handles the password reset process by checking token is valid and not
    expired, then allows the user to set a new password.
    '''
    try:
        hashed_token = hashlib.sha1(token.encode()).hexdigest()
        user_token = ResetToken.objects.get(token=hashed_token, used=False)

        # Check expiry
        if user_token.expiry_date.replace(tzinfo=None) < datetime.now():
            user_token.delete()
            user_token = None
        else:
            # Add to session as per your logic
            request.session["user"] = user_token.user.username
            request.session["token"] = token
    except ResetToken.DoesNotExist:
        user_token = None

    return render(
        request, "ecommerce/password_reset.html", {"token": user_token}
    )


def reset_password_submit(request):
    '''
    Handles submit of new password, by validating token again and then
    changing the user's password. It also marks the token as used and clears
    the session.
    '''
    username = request.session.get("user")
    token = request.session.get("token")
    password = request.POST.get("password")
    password_conf = request.POST.get("password_conf")

    if password == password_conf and username and token:
        change_user_password(username, password)

        hashed_token = hashlib.sha1(token.encode()).hexdigest()
        ResetToken.objects.filter(token=hashed_token).delete()

        del request.session["user"]
        del request.session["token"]

        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(
            reverse("password_reset", kwargs={"token": token})
        )

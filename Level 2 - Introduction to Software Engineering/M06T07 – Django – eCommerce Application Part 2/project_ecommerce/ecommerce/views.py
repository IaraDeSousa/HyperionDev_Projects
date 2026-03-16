from datetime import datetime
import hashlib
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    StoreSerializer,
    ProductSerializer,
    ReviewSerializer,
    UserSerializer,
)
from .models import Product, Purchase, Review, Store
from .models import ResetToken
from .tweet import Tweet
from .forgot_password import (
    build_email,
    generate_reset_url,
    change_user_password,
)


def product_list(request):
    """
    View to display a list of all products available in the database.
    """
    products = Product.objects.select_related("store").all()

    return render(
        request, "ecommerce/product_list.html", {"products": products}
    )


def login_user(request):
    """
    Handles user login using username and password. If successful, the user is
    redirected to the product list page. If the credentials are incorrect, an
    error is displayed.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {username}!")
            print(f"User {username} logged in successfully.")
            return redirect("product_list")
        else:
            return render(
                request,
                "ecommerce/login.html",
                {"error": "Invalid credentials"},
            )

    return render(request, "ecommerce/login.html")


def logout_user(request):
    """
    Logs out the current user and redirects to the login page.
    """
    if request.user is not None:
        logout(request)
        messages.info(request, "You have been logged out.")
        print(f"Session ended for user {request.user.username}.")
        return HttpResponseRedirect(reverse("ecommerce:login"))


def register(request):
    """
    User registration view that handles creating a new user account.
    It includes defensive checks for duplicate usernames and password
    confirmation.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        email = request.POST["email"]
        account_type = request.POST.get("account_type")

        # Check for username existing already
        if User.objects.filter(username=username).exists():
            messages.error(
                request, "Registration failed: This username is already taken."
            )
            print(
                f"[REGISTRATION ERROR] {datetime.now()}: "
                f"Attempted duplicate username '{username}'"
            )
            return render(request, "ecommerce/register.html")

        # Check for password matching
        if password != confirm_password:
            messages.error(
                request, "Registration failed: Passwords do not match."
            )
            print(
                f"[REGISTRATION ERROR] {datetime.now()}: "
                f"Password mismatch for user '{username}'"
            )
            return render(request, "ecommerce/register.html")

        try:
            user = User.objects.create_user(
                username=username, password=password, email=email
            )

            group, created = Group.objects.get_or_create(name=account_type)
            user.groups.add(group)

            if account_type == "vendor":
                store_name = f"{user.username}'s Shop"
                Store.objects.create(vendor=user, name=store_name)

            user.save()

            # User interface feedback that registration was successful.
            # Backend log to confirm registration and account type created.
            messages.success(
                request, f"Account created successfully! Welcome, {username}."
            )
            print(f"New {account_type} created: {username}")

            login(request, user)
            return redirect("product_list")

        except Exception as e:
            messages.error(
                request, "An unexpected error occurred during registration."
            )
            print(f"Registration failed for {username}: {e}")
            return render(request, "ecommerce/register.html")
    return render(request, "ecommerce/register.html")


@login_required
def vendor_hub(request):
    """Shows the vendor's dashboard with their stores and products."""
    my_stores = Store.objects.filter(vendor=request.user)
    return render(
        request, "ecommerce/vendor_hub.html", {"my_stores": my_stores}
    )


@login_required
def create_stores(request):
    """
    Creates a new store for the vendor.
    Creates a post about the new store and posts it to X.
    Note: Currently X is not allowing free accounts to post tweets via
    API, so this may not work without credits.
    """
    if request.method == "POST":
        name = request.POST.get("store_name")
        if name:
            new_store = Store.objects.create(vendor=request.user, name=name)
            tweet_text = f"New store open on The Shop!\n{new_store.name}\n\n"
            tweet_payload = {"text": tweet_text}
            try:
                Tweet().make_tweet(tweet_payload)
            except Exception as e:
                print(f"Tweet failed: {e}")
    return redirect("vendor_hub")


@login_required
def add_products(request):
    """
    Adds a new product to a specific store owned by the vendor.
    Creates a post about the new product and posts it to X.
    Note: Currently X is not allowing free accounts to post tweets via
    API, so this may not work without credits.
    """
    if request.method == "POST":
        store_id = request.POST.get("store_id")
        store = Store.objects.get(id=store_id)

        new_product = Product.objects.create(
            store=store,
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
        )
        product_tweet_text = (
            f"New Item at {store.name}!\n"
            f"Product: {new_product.name}\n"
            f"Description: a new product in The Shop!"
        )

        tweet_payload = {"text": product_tweet_text}

        try:
            Tweet().make_tweet(tweet_payload)
        except Exception as e:
            print(f"Tweet failed: {e}")
    return redirect("vendor_hub")


@login_required
def view_stores(request, store_id):
    """Displays products for a specific store owned by the vendor."""
    store = Store.objects.get(id=store_id, vendor=request.user)
    products = Product.objects.filter(store=store)

    return render(
        request,
        "ecommerce/store_detail.html",
        {"store": store, "products": products},
    )


@login_required
def change_stores(request, store_id):
    """Allows the vendor to edit the name of one of their selected stores."""
    store = Store.objects.get(id=store_id, vendor=request.user)

    if request.method == "POST":
        store.name = request.POST.get("store_name")
        store.save()
        return redirect("store_detail", store_id=store.id)

    return render(request, "ecommerce/edit_store.html", {"store": store})


@login_required
def delete_stores(request, store_id):
    """Allows the vendor to delete one of their selected stores and all
    products in that store."""
    store = Store.objects.get(id=store_id, vendor=request.user)
    store.delete()
    return redirect("vendor_hub")


@login_required
def delete_products(request, product_id):
    """
    Allows the vendor to delete one of their products within a given store.
    """
    product = Product.objects.get(id=product_id, store__vendor=request.user)
    store_id = product.store.id
    product.delete()
    return redirect("store_detail", store_id=store_id)


@login_required
def change_products(request, product_id):
    """
    Allows the vendor to edit the details of one of their products
    within a given store.
    """
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
    """
    Allows a buyer to add a product to their shopping cart, which is
    stored in the session.
    """
    cart = request.session.get("cart", {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session["cart"] = cart

    # To show backend indication that this was successful.
    print(
        f"Username {request.user.username} added product "
        f"{product_id} to cart. Current cart: {cart}"
    )

    # User interface feedback that the item was added to the cart successfully.
    messages.success(request, "Product added to cart successfully!")

    return redirect("product_list")


@login_required
def view_cart(request):
    """
    Displays the contents of the buyer's shopping cart, including product
    details and total cost.
    """
    cart = request.session.get("cart", {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

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
        messages.warning(request, "Your cart is empty.")
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

    # To show backend indication that checkout was successful and
    # what was purchased.
    print(
        f"Username {request.user.username} checked out with "
        f"items:\n{items_list}Total: ${total}"
    )

    # Email logic
    subject = "Your Invoice from THE SHOP"
    message = (
        f"Hi {request.user.username},\n\n"
        f"Order Summary:\n{items_list}"
        f"Total: ${total}\n\n"
        f"Thanks for shopping!"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=True,
    )

    # Backend indication that email was sent successfully.
    print(f"Invoice email sent to {request.user.email}")

    request.session["cart"] = {}
    messages.success(
        request, "Checkout successful! An invoice has been sent to your email."
    )

    return redirect("product_list")


def product_reviews(request, product_id):
    """
    Displays reviews for a specific product and allows all users to
    submit a review. If a user has purchased the product, their review is
    seen as verified.
    """
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
    """
    Handles the password reset request by generating a reset URL and sending a
    password reset email to the user. If email does not exist, it redirects to
    the login page without revealing that the email is not registered for
    security reasons.
    """
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
    """
    Handles the password reset process by checking token is valid and not
    expired, then allows the user to set a new password.
    """
    try:
        hashed_token = hashlib.sha1(token.encode()).hexdigest()
        user_token = ResetToken.objects.get(token=hashed_token, used=False)

        if user_token.expiry_date.replace(tzinfo=None) < datetime.now():
            user_token.delete()
            user_token = None
        else:
            request.session["user"] = user_token.user.username
            request.session["token"] = token
    except ResetToken.DoesNotExist:
        user_token = None

    return render(
        request, "ecommerce/password_reset.html", {"token": user_token}
    )


def reset_password_submit(request):
    """
    Handles submit of new password, by validating token again and then
    changing the user's password. It also marks the token as used and clears
    the session.
    """
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


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_add_store(request):
    """Allow vendors to create a new store via API."""
    if int(request.data.get("vendor")) == request.user.id:
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {"error": "User ID mismatch"}, status=status.HTTP_403_FORBIDDEN
    )


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_add_product(request):
    """Allow vendors to add products to a store they own."""
    store_id = request.data.get("store")
    try:
        Store.objects.get(id=store_id, vendor=request.user)
    except Store.DoesNotExist:
        return Response(
            {"error": "Store not found or unauthorized"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_get_vendor_stores(request, vendor_id):
    """Retrieve all stores for a specific vendor."""
    stores = Store.objects.filter(vendor_id=vendor_id)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_get_store_products(request, store_id):
    """Retrieve all products for a specific store."""
    products = Product.objects.filter(store_id=store_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_get_product_reviews(request, product_id):
    """Retrieve reviews for a specific product."""
    reviews = Review.objects.filter(product_id=product_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_get_all_vendors(request):
    """Fetch all users who belong to the 'vendor' group."""
    vendors = User.objects.filter(groups__name="vendor")

    serializer = UserSerializer(vendors, many=True)
    return Response(serializer.data)

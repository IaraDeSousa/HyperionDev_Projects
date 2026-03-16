from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Password reset URLs
    path(
        "password_reset_request/",
        views.send_password_reset,
        name="password_reset_request",
    ),
    path(
        "reset_password/<str:token>/",
        views.reset_user_password,
        name="password_reset",
    ),
    path(
        "reset_password_submit/",
        views.reset_password_submit,
        name="reset_password_submit",
    ),
    # Vendor hub URLs
    path("vendor/", views.vendor_hub, name="vendor_hub"),
    path("vendor/create-store/", views.create_stores, name="create_store"),
    path("vendor/add-product/", views.add_products, name="add_product"),
    path("store/<int:store_id>/", views.view_stores, name="store_detail"),
    # Vendor Product URLs
    path(
        "product/delete/<int:product_id>/",
        views.delete_products,
        name="delete_product",
    ),
    path(
        "product/edit/<int:product_id>/",
        views.change_products,
        name="edit_product",
    ),
    # Vendor store URLs
    path("store/edit/<int:store_id>/", views.change_stores, name="edit_store"),
    path(
        "store/delete/<int:store_id>/",
        views.delete_stores,
        name="delete_store",
    ),
    # Cart URLs
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    # Review URL
    path(
        "product/<int:product_id>/reviews/",
        views.product_reviews,
        name="product_reviews",
    ),
    # API URLs
    path("api/add-store/", views.api_add_store, name="api_add_store"),
    path("api/add-product/", views.api_add_product, name="api_add_product"),
    path("api/vendor/<int:vendor_id>/stores/", views.api_get_vendor_stores),
    path("api/store/<int:store_id>/products/", views.api_get_store_products),
    path(
        "api/product/<int:product_id>/reviews/", views.api_get_product_reviews
    ),
    path("api/vendors/", views.api_get_all_vendors, name="api_vendors"),
    # Home page URL
    path("", views.product_list, name="product_list"),
]

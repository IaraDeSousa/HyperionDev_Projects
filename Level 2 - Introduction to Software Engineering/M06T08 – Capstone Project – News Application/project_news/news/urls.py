from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path(
        "article/<int:article_id>/",
        views.article_detail,
        name="article_detail",
    ),
    path(
        "article/<int:article_id>/edit/",
        views.edit_article,
        name="edit_article",
    ),
    path(
        "article/<int:article_id>/delete/",
        views.delete_article,
        name="delete_article",
    ),
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path(
        "journalist/", views.journalist_dashboard, name="journalist_dashboard"
    ),
    path(
        "journalist/newsletter/", views.send_newsletter, name="send_newsletter"
    ),
    path(
        "reset-password/",
        views.send_password_reset,
        name="password_reset_request",
    ),
    path(
        "reset-password/<str:token>/",
        views.reset_user_password,
        name="password_reset",
    ),
    path(
        "reset-password-submit/",
        views.reset_password_submit,
        name="reset_password_submit",
    ),
    path("editor/", views.editor_dashboard, name="editor_dashboard"),
    path(
        "editor/approve/<int:article_id>/",
        views.approve_article,
        name="approve_article",
    ),
    path("newsletters/", views.newsletter_list, name="newsletter_list"),
    path(
        "newsletters/<int:newsletter_id>/edit/",
        views.edit_newsletter,
        name="edit_newsletter",
    ),
    path(
        "newsletters/<int:newsletter_id>/delete/",
        views.delete_newsletter,
        name="delete_newsletter",
    ),
    path(
        "newsletters/<int:newsletter_id>/resend/",
        views.resend_newsletter,
        name="resend_newsletter",
    ),
    path("my-subscriptions/", views.my_subscriptions, name="my_subscriptions"),
    # API URLs
    path(
        "api/articles/subscribed/",
        views.api_get_subscribed_articles,
        name="api_subscribed_articles",
    ),
    path(
        "api/articles/publisher/<int:publisher_id>/",
        views.api_get_publisher_articles,
        name="api_publisher_articles",
    ),
    path(
        "api/articles/journalist/<int:journalist_id>/",
        views.api_get_journalist_articles,
        name="api_journalist_articles",
    ),
    path(
        "api/publishers/",
        views.api_get_all_publishers,
        name="api_all_publishers",
    ),
]

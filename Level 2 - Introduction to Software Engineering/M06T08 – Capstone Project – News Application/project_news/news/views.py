"""
This module contains the view logic for the news application, 
handling article displays, user authentication, and dashboards.
"""
import hashlib
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Publisher, Subscription, Newsletter, ResetToken
from .serializers import ArticleSerializer, PublisherSerializer
from .forgot_password import (
    generate_reset_url,
    build_email,
    change_user_password,
)
from .tweet import Tweet


def article_list(request):
    """
    Displays all articles that have been approved by an editor.
    This matches your 'LATEST HEADLINES' template logic.
    """
    articles = (
        Article.objects.filter(is_approved=True)
        .select_related("author", "publisher")
        .order_by("-created_at")
    )
    return render(request, "news/article_list.html", {"articles": articles})


def login_user(request):
    """
    Handles user login using username and password. If successful, the user is
    redirected to the article list page. If the credentials are incorrect, an
    error is displayed.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("article_list")
        else:
            return render(
                request,
                "news/login.html",
                {"error": "Invalid credentials"},
            )

    return render(request, "news/login.html")


def logout_user(request):
    """
    Logs out the current user and redirects to the login page.
    """
    if request.user is not None:
        logout(request)
        return HttpResponseRedirect(reverse("article_list"))


def register(request):
    """
    Handles two-step registration:
    Step 1: Basic info + Role selection.
    Step 2: Publisher affiliation (for Journalists/Editors only).
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        account_type = request.POST.get("account_type")
        step = request.POST.get("step")

        if not step and password != confirm_password:
            return render(
                request,
                "news/register.html",
                {
                    "error": "Passwords do not match",
                    "publishers": Publisher.objects.all(),
                },
            )

        if account_type == "reader" or step == "2":
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            group, _ = Group.objects.get_or_create(name=account_type)
            user.groups.add(group)
            user.save()

            if step == "2":
                existing_pub_id = request.POST.get("existing_publisher")
                new_pub_name = request.POST.get("new_publisher_name")

                publisher = None
                if new_pub_name:
                    publisher = Publisher.objects.create(name=new_pub_name)
                elif existing_pub_id and existing_pub_id != "none":
                    publisher = Publisher.objects.get(id=existing_pub_id)

                if publisher:
                    if account_type == "editor":
                        publisher.editors.add(user)
                    elif account_type == "journalist":
                        publisher.journalists.add(user)
                    print(f"[SYSTEM] Linked {username} to {publisher.name}")

            login(request, user)
            return redirect("article_list")

        else:
            return render(
                request,
                "news/register_publisher.html",
                {
                    "username": username,
                    "email": email,
                    "password": password,
                    "account_type": account_type,
                    "publishers": Publisher.objects.all(),
                },
            )

    return render(
        request, "news/register.html", {"publishers": Publisher.objects.all()}
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
    return render(request, "news/password_reset_request.html")


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

    return render(request, "news/password_reset.html", {"token": user_token})


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


@login_required
def journalist_dashboard(request):
    """
    Dashboard for Journalists to view their own articles and
    submit new ones for approval.
    """
    if not request.user.groups.filter(name="journalist").exists():
        return redirect("article_list")

    my_articles = Article.objects.filter(author=request.user).order_by(
        "-created_at"
    )
    publishers = Publisher.objects.filter(journalists=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        pub_id = request.POST.get("publisher")
        publisher = None
        if pub_id and pub_id != "independent":
            publisher = Publisher.objects.get(id=pub_id)

        Article.objects.create(
            title=title,
            content=content,
            author=request.user,
            publisher=publisher,
            is_approved=False,
        )
        return redirect("journalist_dashboard")

    return render(
        request,
        "news/journalist_dashboard.html",
        {"articles": my_articles, "publishers": publishers},
    )


def is_editor(user):
    return user.groups.filter(name="editor").exists()


@login_required
@user_passes_test(is_editor)
def editor_dashboard(request):
    """
    Lists only articles the editor is authorized to approve.
    """
    my_publisher_ids = Publisher.objects.filter(
        editors=request.user
    ).values_list("id", flat=True)

    pending_articles = (
        Article.objects.filter(is_approved=False)
        .filter(
            Q(publisher_id__in=my_publisher_ids) | Q(publisher__isnull=True)
        )
        .order_by("-created_at")
    )

    return render(
        request, "news/editor_dashboard.html", {"articles": pending_articles}
    )


@login_required
@user_passes_test(is_editor)
def approve_article(request, article_id):
    """
    Approves an article if the editor belongs to the article's publisher
    OR if the article is independent.
    """
    article = get_object_or_404(Article, id=article_id)

    is_publisher_editor = (
        article.publisher
        and article.publisher.editors.filter(id=request.user.id).exists()
    )

    is_independent = article.publisher is None

    if not (is_publisher_editor or is_independent):
        messages.error(
            request,
            "You do not have permission to approve articles for other publishers.",
        )
        return redirect("editor_dashboard")

    article.is_approved = True
    article.save()

    subscribers = Subscription.objects.filter(
        Q(subscribed_publisher=article.publisher)
        | Q(subscribed_journalist=article.author)
    ).select_related("reader")

    emails = list(
        set([sub.reader.email for sub in subscribers if sub.reader.email])
    )

    if emails:
        send_mail(
            subject=f"New Article: {article.title}",
            message=f"A new article '{article.title}' has been published!\n\nRead it now on THE NEWS.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=True,
        )

    try:
        twitter = Tweet()
        tweet_text = f"Breaking News: {article.title} published on THE NEWS! #TheNews #Journalism"
        twitter.make_tweet({"text": tweet_text})
        print(f"[SYSTEM] Tweet successfully posted for article {article.id}")
    except Exception as e:
        print(f"[ERROR] Failed to post tweet: {e}")
        messages.warning(
            request, "Article approved, but the X notification failed to post."
        )

    messages.success(
        request, f"Article '{article.title}' has been approved and published."
    )
    return redirect("editor_dashboard")


@login_required
@user_passes_test(lambda u: u.groups.filter(name="journalist").exists())
def send_newsletter(request):
    """
    Creates a newsletter record in the database and sends it to subscribers.
    """
    articles = Article.objects.filter(author=request.user, is_approved=True)

    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_articles")
        subject = request.POST.get(
            "subject", f"Newsletter from {request.user.username}"
        )

        if not selected_ids:
            messages.warning(request, "Please select at least one article.")
            return redirect("send_newsletter")

        newsletter_articles = Article.objects.filter(id__in=selected_ids)

        content_body = f"Newsletter from {request.user.username}\n\n"
        for art in newsletter_articles:
            content_body += f"--- {art.title} ---\n{art.content[:300]}...\n\n"

        Newsletter.objects.create(
            title=subject, content=content_body, author=request.user
        )

        subs = Subscription.objects.filter(subscribed_journalist=request.user)
        emails = [s.reader.email for s in subs if s.reader.email]

        if emails:
            send_mail(
                subject=subject,
                message=content_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
            )
            messages.success(request, "Newsletter archived and dispatched!")
        else:
            messages.success(
                request,
                "Newsletter saved to archive (no subscribers to email).",
            )

        return redirect("newsletter_list")

    return render(
        request, "news/newsletter_create.html", {"articles": articles}
    )


@login_required
def resend_newsletter(request, newsletter_id):
    """
    Resends a previously created newsletter to its subscribers.
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    is_editor = request.user.groups.filter(name="editor").exists()

    if request.user != newsletter.author and not is_editor:
        messages.error(request, "You don't have permission to resend this.")
        return redirect("newsletter_list")

    if request.method == "POST":
        subs = Subscription.objects.filter(
            subscribed_journalist=newsletter.author
        )
        emails = [s.reader.email for s in subs if s.reader.email]

        if emails:
            send_mail(
                subject=f"[RESEND] {newsletter.title}",
                message=newsletter.content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
            )
            messages.success(
                request, f"Newsletter resent to {len(emails)} subscribers."
            )
        else:
            messages.warning(request, "No subscribers found to send to.")

        return redirect("newsletter_list")

    return redirect("newsletter_list")


@login_required
def article_detail(request, article_id):
    """
    Displays article details and allows readers to subscribe to the author or publisher.
    """
    article = Article.objects.get(id=article_id)

    if request.method == "POST":
        follow_journalist = request.POST.get("follow_journalist")
        follow_publisher = request.POST.get("follow_publisher")

        if follow_journalist:
            Subscription.objects.get_or_create(
                reader=request.user, subscribed_journalist=article.author
            )
            messages.success(
                request, f"Subscribed to {article.author.username}!"
            )
            print(
                f"[SUB] {request.user.username} -> Journalist: {article.author.username}"
            )

        if follow_publisher:
            if article.publisher:
                Subscription.objects.get_or_create(
                    reader=request.user, subscribed_publisher=article.publisher
                )
                messages.success(
                    request, f"Subscribed to {article.publisher.name}!"
                )
                print(
                    f"[SUB] {request.user.username} -> Publisher: {article.publisher.name}"
                )
            else:
                messages.error(
                    request, "This article has no associated publisher."
                )

    return render(request, "news/article_detail.html", {"article": article})


@login_required
def my_subscriptions(request):
    """
    Displays the user's current subscriptions and allows them to unsubscribe.
    """
    subs = Subscription.objects.filter(reader=request.user).select_related(
        "subscribed_journalist", "subscribed_publisher"
    )

    if request.method == "POST":
        sub_id = request.POST.get("subscription_id")
        subscription = get_object_or_404(
            Subscription, id=sub_id, reader=request.user
        )

        name = (
            subscription.subscribed_journalist.username
            if subscription.subscribed_journalist
            else subscription.subscribed_publisher.name
        )

        subscription.delete()
        messages.success(request, f"Unfollowed {name}.")
        return redirect("my_subscriptions")

    return render(
        request, "news/my_subscriptions.html", {"subscriptions": subs}
    )


@login_required
def newsletter_list(request):
    """
    Editors see all newsletters. Journalists see only theirs.
    """
    is_editor = request.user.groups.filter(name="editor").exists()

    if is_editor:
        newsletters = Newsletter.objects.all().order_by("-created_at")
    elif request.user.groups.filter(name="journalist").exists():
        newsletters = Newsletter.objects.filter(author=request.user).order_by(
            "-created_at"
        )
    else:
        return redirect("article_list")

    return render(
        request, "news/newsletter_list.html", {"newsletters": newsletters}
    )


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    is_authorized_editor = (
        article.publisher
        and article.publisher.editors.filter(id=request.user.id).exists()
    )

    if request.user != article.author and not is_authorized_editor:
        messages.error(
            request, "You can only edit articles for your own publisher."
        )
        return redirect("article_detail", article_id=article.id)

    if request.method == "POST":
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.save()
        messages.success(request, "Article updated successfully.")
        return redirect("article_detail", article_id=article.id)

    return render(request, "news/edit_article.html", {"article": article})


@login_required
def delete_article(request, article_id):
    """
    Deletes an article if the user is the author or an editor for the article's publisher.
    """
    article = get_object_or_404(Article, id=article_id)

    is_authorized_editor = (
        article.publisher
        and article.publisher.editors.filter(id=request.user.id).exists()
    )

    if request.user == article.author or is_authorized_editor:
        if request.method == "POST":
            article.delete()
            messages.success(request, "Article deleted.")
            return redirect("article_list")

    return redirect("article_detail", article_id=article.id)


@login_required
def edit_newsletter(request, newsletter_id):
    """ "
    Allows the author of the newsletter or an editor from the same publisher group to edit the newsletter content.
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    is_authorized_editor = Publisher.objects.filter(
        editors=request.user, journalists=newsletter.author
    ).exists()

    if request.user != newsletter.author and not is_authorized_editor:
        messages.error(
            request,
            "Permission denied: This author is not in your publisher group.",
        )
        return redirect("newsletter_list")

    if request.method == "POST":
        newsletter.title = request.POST.get("subject")
        newsletter.content = request.POST.get("content")
        newsletter.save()
        messages.success(request, "Archive updated.")
        return redirect("newsletter_list")

    return render(
        request, "news/edit_newsletter.html", {"newsletter": newsletter}
    )


@login_required
def delete_newsletter(request, newsletter_id):
    """
    Deletes a newsletter if the user is the author or an editor from the same publisher group.
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    is_authorized_editor = Publisher.objects.filter(
        editors=request.user, journalists=newsletter.author
    ).exists()

    if request.user == newsletter.author or is_authorized_editor:
        if request.method == "POST":
            newsletter.delete()
            messages.success(request, "Newsletter removed from archive.")
            return redirect("newsletter_list")

    return redirect("newsletter_list")


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_get_subscribed_articles(request):
    """
    Retrieve articles from publishers and journalists
    that the authenticated user has subscribed to.
    """
    user = request.user

    subs = Subscription.objects.filter(reader=user)
    followed_journalists = subs.values_list("subscribed_journalist", flat=True)
    followed_publishers = subs.values_list("subscribed_publisher", flat=True)

    articles = (
        Article.objects.filter(
            Q(author_id__in=followed_journalists)
            | Q(publisher_id__in=followed_publishers),
            is_approved=True,
        )
        .distinct()
        .order_by("-created_at")
    )

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_get_publisher_articles(request, publisher_id):
    """Retrieve all approved articles for a specific publisher."""
    articles = Article.objects.filter(
        publisher_id=publisher_id, is_approved=True
    )
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_get_journalist_articles(request, journalist_id):
    """Retrieve all approved articles for a specific journalist."""
    articles = Article.objects.filter(
        author_id=journalist_id, is_approved=True
    )
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_get_all_publishers(request):
    """Fetch all publishers registered in the system."""
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, many=True)
    return Response(serializer.data)

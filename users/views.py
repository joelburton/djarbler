from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from djarbler.forms import CsrfOnlyForm
from users.forms import SignupForm, ProfileForm
from users.models import User


def signup(request):
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = User.signup(**form.cleaned_data)
            login(request, u)
            messages.success(request, "Registered and logged in.")
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile(request):
    """Update profile for current user."""

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Edited profile.")
            return redirect(f"/users/{request.user.id}/")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "users/edit.html", {"form": form})


@login_required
def list_users(request):
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    if q := request.GET.get("q"):
        users = User.objects.filter(username__icontains=q).all()
    else:
        users = User.objects.filter().all()

    return render(request, 'users/index.html', {"users": users})


@login_required
def users_show(request, user_id):
    """Show user profile."""

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/show.html', {"user": user})


@login_required
def show_following(request, user_id):
    """Show list of people this user is following."""

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/following.html', {"user": user})


@login_required
def users_followers(request, user_id):
    """Show list of followers of this user."""

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/followers.html', {"user": user})


@login_required
def add_follow(request, follow_id):
    """Add a follow for the currently-logged-in user."""

    form = CsrfOnlyForm(request.POST)
    if request.method != "POST" or not form.is_valid():
        raise PermissionDenied()

    user: User = request.user
    followed_user = get_object_or_404(User, pk=follow_id)
    user.following.add(followed_user)
    messages.info(request, "Added following.")

    return redirect(f"/users/{user.id}/following/")


@login_required
def stop_following(request, follow_id):
    """Have currently-logged-in-user stop following this user."""

    form = CsrfOnlyForm(request.POST)
    if request.method != "POST" or not form.is_valid():
        raise PermissionDenied()

    user: User = request.user
    followed_user = get_object_or_404(User, pk=follow_id)
    user.following.remove(followed_user)
    messages.info(request, "Stop following.")

    return redirect(f"/users/{user.id}/following/")


@login_required
def show_likes(request, user_id):
    """Show likes for a user."""

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/likes.html', {"user": user})


@login_required
def delete_user(request):
    """Delete user."""

    form = CsrfOnlyForm(request.POST)
    if request.method != "POST" or not form.is_valid():
        raise PermissionDenied()

    request.user.delete()
    messages.warning(request, "Go back to Twitter, loser!")

    return redirect("/users/signup/")

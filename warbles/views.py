from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404

from djarbler.forms import CsrfOnlyForm
from users.models import User
from .forms import MessageCreateForm
from .models import Message


@login_required
def create(request):
    """Create a new message."""

    if request.method == "POST":
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "Warble saved.")
            return redirect("/")
    else:
        form = MessageCreateForm()
    return render(request, "warbles/new.html", {"form": form})


@login_required
def messages_show(request, message_id):
    """Show a message."""

    msg = get_object_or_404(Message, pk=message_id)
    return render(request, 'warbles/show.html', {"message": msg})


@login_required
def messages_destroy(request, message_id):
    """Delete a message."""

    form = CsrfOnlyForm(request.POST)
    msg = get_object_or_404(Message, pk=message_id)

    if (request.method != "POST" or
            not form.is_valid() or
            msg.user != request.user):
        raise PermissionDenied()

    messages.warning(request, "Message deleted.")
    msg.delete()

    return redirect(f"/users/{request.user.id}/")


@login_required
def toggle_like(request, message_id):
    """Toggle a liked message for the currently-logged-in user."""

    form = CsrfOnlyForm(request.POST)
    user: User = request.user

    if request.method != "POST" or not form.is_valid():
        raise PermissionDenied()

    liked_message = get_object_or_404(Message, pk=message_id)
    if liked_message.user == user:
        raise PermissionDenied(
            "You're so vain, you probably think this error is about you.")

    if user.liked_messages.contains(liked_message):
        messages.success(request, "Un-liked.")
        user.liked_messages.remove(liked_message)
    else:
        messages.success(request, "Liked.")
        user.liked_messages.add(liked_message)

    return redirect("/")

from django.db.models import Q
from django.shortcuts import render

from users.models import User
from warbles.models import Message


def homepage(request):
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    user: User = request.user

    if request.user.is_authenticated:
        msgs = (Message
                .objects
                .filter(Q(user__in=user.following.all()) | Q(user=user))
                .order_by("-timestamp"))[:100]

        return render(request, "home.html", {"warbles": msgs})

    else:
        return render(request, "home-anon.html")

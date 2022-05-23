from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_users),
    path("signup/", views.signup),
    path("profile/", views.profile),
    path("delete/", views.delete_user),

    path("<int:user_id>/", views.users_show),
    path("<int:user_id>/following/", views.show_following),
    path("<int:user_id>/followers/", views.users_followers),
    path("<int:user_id>/likes/", views.show_likes),

    path("follow/<int:follow_id>/", views.add_follow),
    path("stop-following/<int:follow_id>/", views.stop_following),
]

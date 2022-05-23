from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create),
    path("<int:message_id>/", views.messages_show),
    path("<int:message_id>/like/", views.toggle_like),
    path("<int:message_id>/delete", views.messages_destroy),
]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.homepage),
    path('accounts/', include('django.contrib.auth.urls')),
    path('messages/', include('warbles.urls')),
    path('users/', include('users.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

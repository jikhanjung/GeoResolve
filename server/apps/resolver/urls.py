from django.urls import path
from .views import ResolveView, PingView


urlpatterns = [
    path("resolve/", ResolveView.as_view(), name="resolve"),
    path("ping/", PingView.as_view(), name="ping"),
]


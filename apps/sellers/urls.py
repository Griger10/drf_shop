from django.urls import path

from apps.sellers import views

urlpatterns = [
    path("", views.SellersView.as_view())
]

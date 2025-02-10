from django.urls import path

from apps.sellers import views
from apps.sellers.views import ProductsBySellerView, SellerProductView

urlpatterns = [
    path("", views.SellersView.as_view()),
    path("products/", ProductsBySellerView.as_view()),
    path("sellers_products/", SellerProductView.as_view())
]

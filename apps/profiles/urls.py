from django.urls import path

from apps.profiles import views

urlpatterns = [
    path('', views.ProfileView.as_view()),
    path('shipping_addresses/', views.ShippingAddressesView.as_view()),
    path('shipping_addresses/detail/<uuid:pk>/', views.ShippingAddressViewID.as_view())
]

from django.urls import path

from apps.shop import views

urlpatterns = [
    path('categories/', views.CategoriesView.as_view())
]
from django.urls import path

from .views import CategoryDetailAPIView, CategoryListCreateAPIView

urlpatterns = [
    path("", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("<slug:slug>/", CategoryDetailAPIView.as_view(), name="category-detail"),
]

# jobs/urls.py
from django.urls import path
from .views import JobListCreateAPIView, JobDetailAPIView, CategoryListCreateAPIView, CategoryDetailAPIView

urlpatterns = [
    path('', JobListCreateAPIView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
]

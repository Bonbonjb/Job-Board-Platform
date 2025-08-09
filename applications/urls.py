from django.urls import path
from .views import ApplicationListCreateAPIView, ApplicationDetailAPIView
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path('', ApplicationListCreateAPIView.as_view(), name='application-list-create'),
    path('<int:pk>/', ApplicationDetailAPIView.as_view(), name='application-detail'),
]

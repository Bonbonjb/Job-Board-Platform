from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer
from applications.models import Application
from applications.serializers import ApplicationSerializer
from .models import Category
from .serializers import CategorySerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from django.shortcuts import render


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission: Only admins/staff can modify, others read-only."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.select_related('category', 'posted_by')
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['location', 'category', 'is_active', 'job_type']
    search_fields = ['title', 'company', 'location']
    ordering_fields = ['date_posted', 'salary']
    ordering = ['-date_posted']


class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related('category', 'posted_by')
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrReadOnly]


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.select_related('job', 'user')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admins see all applications, users see only their own
        user = self.request.user
        if user.is_staff:
            return Application.objects.select_related('job', 'user')
        return Application.objects.select_related('job', 'user').filter(user=user)

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        user = self.request.user

        # Prevent duplicate applications for the same job
        if Application.objects.filter(job=job, user=user).exists():
            raise serializers.ValidationError("You have already applied for this job.")

        serializer.save(user=user)


class ApplicationDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.select_related('job', 'user')
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            # Only admin can change status
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can create

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can update/delete

@extend_schema(exclude=True)
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list-create', request=request, format=format),
        'jobs': reverse('job-list-create', request=request, format=format),
        'applications': reverse('application-list-create', request=request, format=format),
        'categories': reverse('category-list-create', request=request, format=format),
    })

    def index(request):
        return render(request, "index.html")    
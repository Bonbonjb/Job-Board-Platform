from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer
from jobs.tasks import send_application_email
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Application.objects.all()

        if user.is_authenticated:
            return Application.objects.filter(
                job__posted_by=user
            ) | Application.objects.filter(user=user)

        return Application.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]  # Require login to view

    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)

        job = application.job
        job_poster_email = job.posted_by.email
        applicant_email = self.request.user.email

        print("📬 Calling email task...")

        send_application_email.delay(
            job_title=job.title,
            applicant_email=applicant_email,
            employer_email=job_poster_email
        )


class ApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Application.objects.all()

        if user.is_authenticated:
            return Application.objects.filter(
                job__posted_by=user
            ) | Application.objects.filter(user=user)

        return Application.objects.none()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]  # Require login for detail

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        job = application.job
        user = request.user

        # Only the job poster or staff can change the status
        if 'status' in request.data:
            if job.posted_by != user and not user.is_staff:
                return Response(
                    {'detail': 'You do not have permission to change the application status.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Prevent applicants from modifying their own application after submission
        if application.user == user and 'status' not in request.data:
            return Response(
                {'detail': 'You cannot modify your application after submission.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        application = self.get_object()
        if application.user != request.user:
            return Response({'detail': 'You can only delete your own application.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
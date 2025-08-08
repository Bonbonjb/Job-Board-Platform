from rest_framework import generics
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework import permissions
from jobs.tasks import send_application_email


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)

        job = application.job
        job_poster_email = job.posted_by.email  # assumes Job has a ForeignKey to CustomUser
        applicant_email = self.request.user.email

        print("📬 Calling email task...")

        send_application_email.delay(
            job_title=job.title,
            applicant_email=applicant_email,
            employer_email=job_poster_email
        )


class ApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]



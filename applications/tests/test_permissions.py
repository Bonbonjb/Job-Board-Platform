from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from jobs.models import Job
from applications.models import Application


class ApplicationPermissionsTest(APITestCase):

    def setUp(self):
        # Users
        self.staff_user = CustomUser.objects.create_user(
            email="admin@example.com", password="pass1234", is_staff=True
        )
        self.employer = CustomUser.objects.create_user(
            email="employer@example.com", password="pass1234"
        )
        self.applicant = CustomUser.objects.create_user(
            email="applicant@example.com", password="pass1234"
        )
        self.other_user = CustomUser.objects.create_user(
            email="other@example.com", password="pass1234"
        )

        # Job posted by employer
        self.job = Job.objects.create(
            title="Backend Developer",
            description="Job description",
            posted_by=self.employer
        )

        # Application submitted by applicant
        self.application = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="My cover letter"
        )

        self.list_url = reverse("application-list-create")
        self.detail_url = reverse("application-detail", args=[self.application.id])

    def test_staff_can_view_all_applications(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_employer_can_view_applications_for_their_jobs(self):
        self.client.force_authenticate(user=self.employer)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_applicant_can_view_their_own_applications(self):
        self.client.force_authenticate(user=self.applicant)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_other_user_cannot_view_applications(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 0)

    def test_employer_can_update_status(self):
        self.client.force_authenticate(user=self.employer)
        response = self.client.patch(self.detail_url, {"status": "accepted"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, "accepted")

    def test_applicant_cannot_update_status(self):
        self.client.force_authenticate(user=self.applicant)
        response = self.client.patch(self.detail_url, {"status": "accepted"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_applicant_can_delete_their_application(self):
        self.client.force_authenticate(user=self.applicant)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete_application(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

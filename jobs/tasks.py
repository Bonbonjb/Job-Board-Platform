from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_application_email(job_title, applicant_email, employer_email):
    print(f"📧 Sending application email for job: {job_title}")
    print(f"From: {applicant_email} → To: {employer_email}")

    subject = f"New Application for {job_title}"
    message = f"You have received a new application from {applicant_email} for your job posting: {job_title}."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [employer_email]

    send_mail(subject, message, from_email, recipient_list)
    print("Email sent successfully.")
    return "Email sent"

from django.db import models
from django.conf import settings
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    company = models.CharField(max_length=200, db_index=True)
    location = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobs', db_index=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posted_jobs', db_index=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'location']),
            models.Index(fields=['category', 'job_type']),
            models.Index(fields=['is_active', 'date_posted']),
        ]

    def __str__(self):
        return self.title
# scripts/seed_data.py
from django.utils.timezone import now
from jobs.models import Category, Job
from users.models import CustomUser
from django.contrib.auth.hashers import make_password

def run():
    print("Seeding data...")

    # --- Seed categories ---
    category_names = [
        "Engineering", "Marketing", "Design", "Finance",
        "IT Support", "Legal"
    ]
    categories = []
    for name in category_names:
        cat, _ = Category.objects.get_or_create(name=name)
        categories.append(cat)
    print(f"{len(categories)} categories added.")

    # --- Seed users ---
    users = [
        ("alice", "alice@example.com", "alicepass123"),
        ("bob", "bob@example.com", "bobpass123"),
        ("charlie", "charlie@example.com", "charliepass123"),
    ]
    user_objs = []
    for username, email, raw_password in users:
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "password": make_password(raw_password)
            }
        )
        user_objs.append(user)
    print(f"{len(user_objs)} users added.")

    # --- Seed jobs ---
    sample_jobs = [
        {
            "title": "Backend Developer",
            "company": "TechHive",
            "location": "Nairobi",
            "description": "Develop scalable APIs using Django.",
            "category": categories[0],  # Engineering
            "salary": 150000,
        },
        {
            "title": "UI/UX Designer",
            "company": "CreativeStudio",
            "location": "Mombasa",
            "description": "Design user interfaces and improve user experience.",
            "category": categories[2],  # Design
            "salary": 95000,
        },
        {
            "title": "Digital Marketer",
            "company": "Brandly",
            "location": "Kisumu",
            "description": "Manage social media and SEO campaigns.",
            "category": categories[1],  # Marketing
            "salary": 85000,
        },
    ]

    for i, job_data in enumerate(sample_jobs):
        Job.objects.get_or_create(
            title=job_data["title"],
            company=job_data["company"],
            defaults={
                "location": job_data["location"],
                "description": job_data["description"],
                "category": job_data["category"],
                "salary": job_data["salary"],
                "is_active": True,
                "date_posted": now(),
                "posted_by": user_objs[i % len(user_objs)]
            }
        )
    print(f"{len(sample_jobs)} jobs added.")

    print("Done seeding data.")
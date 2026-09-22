from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    VERIFICATION_CHOICES = (
        ('Unverified', 'Unverified'),
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    )
    DOCUMENT_TYPES = (
        ('Driving License', 'Driving License'),
        ('Aadhaar Card', 'Aadhaar Card'),
        ('Passport', 'Passport'),
        ('Voter ID', 'Voter ID'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    # Document Verification Fields
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default='Unverified')
    id_document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='Driving License')
    id_number = models.CharField(max_length=50, blank=True, null=True)
    document_file = models.CharField(max_length=255, blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.verification_status}"

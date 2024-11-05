from django.db import models

# from django.conf import settings

# User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model

User = get_user_model()

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)

DOCUMENT_TYPE_CHOICES = (
    ("NIN", "NIN"),
    ("Voter's Card", "Voter's Card"),
    ("Passport", "Passport"),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=60, blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, blank=True)
    front_cover = models.ImageField(upload_to="document_front_cover", blank=True)    
    back_cover = models.ImageField(upload_to="document_back_cover", blank=True)    

    def __str__(self) -> str:
        return f"{self.user} profile"

# Personal Information:

# Full Name: Legal first and last names.
# Date of Birth: To verify age and eligibility.
# Gender: Optional, for demographic insights.
# Nationality: To determine applicable regulations.
# Contact Details:

# Email Address: For communication and account recovery.
# Phone Number: For two-factor authentication and notifications.
# Residential Address: For identity verification and regulatory compliance.
# Identification Documents:

# Government-Issued ID: Such as a passport, driver's license, or national ID card, to comply with Know Your Customer (KYC) regulations.
# Social Security Number (or equivalent): For tax reporting and identity verification.
# Employment and Financial Information:

# Occupation: To assess financial behavior and risk.
# Employer Details: For income verification.
# Annual Income: To determine financial standing and suitability for certain services.
# Source of Funds: To comply with Anti-Money Laundering (AML) regulations.
# Banking and Payment Details:

# Bank Account Information: For transactions and fund transfers.
# Credit/Debit Card Details: For payments and linking accounts.
# Security Information:

# Username and Password: For account access.
# Security Questions: For account recovery.
# Biometric Data: Optional, for enhanced security measures like fingerprint or facial recognition.
from django.db import models
from django.core.exceptions import ValidationError
import re

# --- Custom Validators ---
def validate_name(value):
    if not re.fullmatch(r'[A-Za-z\s]{3,50}', value):
        raise ValidationError("Name must be 3-50 characters, letters and spaces only.")

def validate_mobile(value):
    if not re.fullmatch(r'\d{10}', value):
        raise ValidationError("Mobile number must be exactly 10 digits.")

def validate_password(value):
    if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$', value):
        raise ValidationError(
            "Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character."
        )

# --- Model ---
class userRegisteredTable(models.Model):
    name = models.CharField(max_length=50, validators=[validate_name])
    email = models.EmailField(unique=True)
    loginid = models.CharField(max_length=30, unique=True)
    mobile = models.CharField(max_length=10, validators=[validate_mobile])
    password = models.CharField(max_length=128, validators=[validate_password])
    status = models.CharField(max_length=20, default='waiting')
    
    # Add image fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
   
    def __str__(self):
        return self.name  # Updated from self.username (which was incorrect)
class Block(models.Model):
    index = models.IntegerField()
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    message = models.TextField()  # Stores encrypted message
    timestamp = models.FloatField()
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    nonce = models.IntegerField()

    def __str__(self):
        return f"Block {self.index}"
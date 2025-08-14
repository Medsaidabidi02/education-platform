from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Extended User model with device tracking and approval system"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Device tracking
    max_devices = models.IntegerField(default=1)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserSession(models.Model):
    """Track user sessions for device management"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    device_fingerprint = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_sessions'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.user.email} - {self.device_fingerprint[:20]}..."
    
    def is_expired(self):
        """Check if session is expired (inactive for more than 24 hours)"""
        return timezone.now() - self.last_activity > timezone.timedelta(hours=24)

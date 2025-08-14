from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Plan(models.Model):
    """Subscription plans for the education platform"""
    
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Features
    max_courses = models.IntegerField(default=0)  # 0 means unlimited
    max_videos_per_course = models.IntegerField(default=0)  # 0 means unlimited
    max_devices = models.IntegerField(default=1)
    video_quality = models.CharField(max_length=10, default='720p')
    download_enabled = models.BooleanField(default=False)
    offline_viewing = models.BooleanField(default=False)
    
    # Duration
    duration_days = models.IntegerField(default=30)  # Plan duration in days
    
    # Status
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plans'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ${self.price}/{self.duration_days} days"


class UserPlan(models.Model):
    """User subscription to plans"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plans')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    
    # Subscription details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    auto_renew = models.BooleanField(default=True)
    
    # Payment tracking
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_plans'
        ordering = ['-created_at']
        unique_together = ['user', 'plan', 'start_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        from django.utils import timezone
        return (
            self.status == 'active' and
            self.start_date <= timezone.now() <= self.end_date
        )

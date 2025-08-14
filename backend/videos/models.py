from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid
from django.utils import timezone

User = get_user_model()


class Video(models.Model):
    """Video model with encryption and security features"""
    
    QUALITY_CHOICES = [
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4k', '4K'),
    ]
    
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='videos')
    
    # Video Details
    order = models.PositiveIntegerField(default=0)  # Order within the course
    duration_seconds = models.PositiveIntegerField(default=0)
    file_size = models.BigIntegerField(default=0)  # Size in bytes
    
    # Media Files
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    
    # Video Quality
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='720p')
    
    # Security and Encryption
    video_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    encrypted_url = models.URLField(blank=True, null=True)
    signing_key = models.CharField(max_length=255, blank=True, null=True)
    is_encrypted = models.BooleanField(default=False)
    
    # Access Control
    is_preview = models.BooleanField(default=False)  # Can be viewed without subscription
    is_downloadable = models.BooleanField(default=False)
    
    # Processing Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    processing_progress = models.PositiveIntegerField(default=0)  # 0-100
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'videos'
        ordering = ['course', 'order']
        indexes = [
            models.Index(fields=['course', 'order']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def generate_signed_url(self, user, expiry_seconds=3600):
        """Generate a signed URL for video access"""
        from django.conf import settings
        import hmac
        import hashlib
        import time
        
        # Check if user can access this video
        if not self.can_user_access(user):
            return None
        
        timestamp = int(time.time()) + expiry_seconds
        
        # Create signature
        message = f"{self.video_id}:{user.id}:{timestamp}"
        signature = hmac.new(
            settings.VIDEO_ENCRYPTION_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"/api/videos/{self.video_id}/stream/?expires={timestamp}&signature={signature}"
    
    def can_user_access(self, user):
        """Check if user can access this video"""
        if self.is_preview:
            return True
        
        if not user.is_authenticated:
            return False
        
        return self.course.can_user_access(user)
    
    @property
    def duration_formatted(self):
        """Return formatted duration (HH:MM:SS)"""
        hours = self.duration_seconds // 3600
        minutes = (self.duration_seconds % 3600) // 60
        seconds = self.duration_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"


class VideoProgress(models.Model):
    """Track user progress on individual videos"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='user_progress')
    
    # Progress tracking
    watched_seconds = models.PositiveIntegerField(default=0)
    last_position = models.PositiveIntegerField(default=0)  # Last watched position in seconds
    is_completed = models.BooleanField(default=False)
    
    # Timestamps
    first_watched = models.DateTimeField(auto_now_add=True)
    last_watched = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'video_progress'
        unique_together = ['user', 'video']
        ordering = ['-last_watched']
    
    def __str__(self):
        return f"{self.user.email} - {self.video.title} ({self.progress_percentage:.1f}%)"
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.video.duration_seconds == 0:
            return 0.0
        return min((self.watched_seconds / self.video.duration_seconds) * 100, 100.0)
    
    def mark_completed(self):
        """Mark video as completed"""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.watched_seconds = self.video.duration_seconds
        self.last_position = self.video.duration_seconds
        self.save()


class VideoAccessLog(models.Model):
    """Log video access for security and analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_access_logs')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='access_logs')
    
    # Access details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_fingerprint = models.CharField(max_length=255, blank=True)
    
    # Session info
    session_id = models.CharField(max_length=255, blank=True)
    access_granted = models.BooleanField(default=True)
    denial_reason = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    accessed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'video_access_logs'
        ordering = ['-accessed_at']
        indexes = [
            models.Index(fields=['user', 'video']),
            models.Index(fields=['accessed_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} accessed {self.video.title} at {self.accessed_at}"

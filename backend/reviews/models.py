from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Review(models.Model):
    """Course review model with moderation"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='reviews')
    
    # Review Content
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Moderation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)
    moderator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='moderated_reviews'
    )
    moderation_notes = models.TextField(blank=True)
    
    # Helpful votes
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['user', 'course']  # One review per user per course
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course', 'is_approved']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.course.title} ({self.rating}/5)"
    
    def approve(self, moderator=None):
        """Approve the review"""
        self.status = 'approved'
        self.is_approved = True
        self.moderator = moderator
        self.moderated_at = models.functions.Now()
        self.save()
    
    def reject(self, moderator=None, reason=""):
        """Reject the review"""
        self.status = 'rejected'
        self.is_approved = False
        self.moderator = moderator
        self.moderation_notes = reason
        self.moderated_at = models.functions.Now()
        self.save()
    
    @property
    def helpfulness_ratio(self):
        """Calculate helpfulness ratio"""
        total_votes = self.helpful_count + self.not_helpful_count
        if total_votes == 0:
            return 0.0
        return (self.helpful_count / total_votes) * 100


class ReviewHelpfulness(models.Model):
    """Track user votes on review helpfulness"""
    
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_votes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpfulness_votes')
    vote = models.CharField(max_length=20, choices=VOTE_CHOICES)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'review_helpfulness'
        unique_together = ['user', 'review']  # One vote per user per review
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} voted '{self.vote}' on {self.review.id}"
    
    def save(self, *args, **kwargs):
        """Override save to update review helpfulness counts"""
        is_new = self.pk is None
        old_vote = None
        
        if not is_new:
            old_vote = ReviewHelpfulness.objects.get(pk=self.pk).vote
        
        super().save(*args, **kwargs)
        
        # Update review counts
        if is_new:
            if self.vote == 'helpful':
                self.review.helpful_count += 1
            else:
                self.review.not_helpful_count += 1
        elif old_vote != self.vote:
            if old_vote == 'helpful':
                self.review.helpful_count -= 1
                self.review.not_helpful_count += 1
            else:
                self.review.helpful_count += 1
                self.review.not_helpful_count -= 1
        
        self.review.save()
    
    def delete(self, *args, **kwargs):
        """Override delete to update review helpfulness counts"""
        if self.vote == 'helpful':
            self.review.helpful_count -= 1
        else:
            self.review.not_helpful_count -= 1
        
        self.review.save()
        super().delete(*args, **kwargs)


class ReviewReport(models.Model):
    """Report inappropriate reviews"""
    
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Review'),
        ('offensive', 'Offensive Language'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_reports')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    
    # Moderation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    moderator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='handled_reports'
    )
    resolution_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'review_reports'
        unique_together = ['reporter', 'review']  # One report per user per review
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.reporter.email} on review {self.review.id}"

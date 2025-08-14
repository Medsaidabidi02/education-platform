from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    """Course categories"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)  # For icon class names
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Course model with plan-based access control"""
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    
    # Course Details
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    
    # Media
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    preview_video = models.URLField(blank=True, null=True)
    
    # Access Control
    required_plans = models.ManyToManyField('plans.Plan', blank=True, related_name='accessible_courses')
    is_free = models.BooleanField(default=False)
    
    # Pricing (if not free and not plan-based)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Course Metadata
    duration_hours = models.PositiveIntegerField(default=0)  # Total duration in hours
    total_lessons = models.PositiveIntegerField(default=0)
    
    # Status and Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # SEO and Analytics
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['category', 'difficulty_level']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0.0
    
    @property
    def total_reviews(self):
        """Count total approved reviews"""
        return self.reviews.filter(is_approved=True).count()
    
    def can_user_access(self, user):
        """Check if user can access this course"""
        if self.is_free:
            return True
        
        if not user.is_authenticated:
            return False
        
        # Check if user has an active plan that includes this course
        user_plans = user.user_plans.filter(status='active')
        for user_plan in user_plans:
            if user_plan.is_active and self.required_plans.filter(id=user_plan.plan.id).exists():
                return True
        
        return False


class Enrollment(models.Model):
    """Track user enrollments in courses"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Progress tracking
    progress_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    completed_lessons = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    
    # Completion
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    certificate_issued = models.BooleanField(default=False)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"

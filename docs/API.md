# API Documentation

## Authentication

### Registration Flow
1. User submits registration form
2. Account created with `is_approved=False`
3. Admin approves account via admin panel
4. User receives approval notification
5. User can login and access content

### Login Flow
1. User provides email/password + device fingerprint
2. System checks device limits
3. JWT tokens generated and stored
4. Session tracking activated
5. Access granted to protected resources

### Device Management
- Each user has a maximum device limit (default: 1)
- Device fingerprinting prevents account sharing
- Sessions automatically expire after 24 hours of inactivity
- Users can view and terminate active sessions

## Video Security

### Signed URLs
```python
# Example signed URL generation
url = video.generate_signed_url(user, expiry_seconds=3600)
# Returns: /api/videos/{uuid}/stream/?expires={timestamp}&signature={hash}
```

### Access Control
- Only authenticated users can access videos
- Plan-based restrictions for premium content
- IP address and user agent logging
- Playback position tracking

## Database Models

### User Model
```python
class User(AbstractUser):
    email = EmailField(unique=True)
    role = CharField(choices=['student', 'instructor', 'admin'])
    is_approved = BooleanField(default=False)
    max_devices = IntegerField(default=1)
```

### Course Model
```python
class Course(Model):
    title = CharField(max_length=200)
    instructor = ForeignKey(User)
    required_plans = ManyToManyField(Plan)
    is_free = BooleanField(default=False)
    status = CharField(choices=['draft', 'published', 'archived'])
```

### Video Model
```python
class Video(Model):
    course = ForeignKey(Course)
    video_id = UUIDField(unique=True)
    is_encrypted = BooleanField(default=False)
    signing_key = CharField(max_length=255)
```

## Error Handling

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

### Error Response Format
```json
{
  "error": "Error message",
  "details": {
    "field": ["Field specific error"]
  }
}
```
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import UserSession
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserSessionSerializer,
    PasswordChangeSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'Registration successful. Please wait for admin approval.',
            'user_id': user.id,
            'email': user.email
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint with device tracking"""
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    device_fingerprint = serializer.validated_data.get('device_fingerprint', '')
    
    # Check device limits
    active_sessions = UserSession.objects.filter(user=user, is_active=True)
    
    # Remove expired sessions
    for session in active_sessions:
        if session.is_expired():
            session.is_active = False
            session.save()
    
    # Refresh active sessions count
    active_sessions = UserSession.objects.filter(user=user, is_active=True)
    
    if active_sessions.count() >= user.max_devices:
        # Check if current device is already logged in
        current_device_session = active_sessions.filter(
            device_fingerprint=device_fingerprint
        ).first()
        
        if not current_device_session:
            return Response({
                'error': 'Maximum device limit reached. Please logout from other devices.',
                'max_devices': user.max_devices,
                'active_devices': active_sessions.count()
            }, status=status.HTTP_403_FORBIDDEN)
    
    # Create or update session
    user_session, created = UserSession.objects.get_or_create(
        user=user,
        device_fingerprint=device_fingerprint,
        defaults={
            'session_key': '',
            'ip_address': request.META.get('REMOTE_ADDR', ''),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'is_active': True
        }
    )
    
    if not created:
        user_session.ip_address = request.META.get('REMOTE_ADDR', '')
        user_session.user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_session.is_active = True
        user_session.last_activity = timezone.now()
        user_session.save()
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    # Store session key in token
    user_session.session_key = str(refresh)
    user_session.save()
    
    return Response({
        'access_token': str(access_token),
        'refresh_token': str(refresh),
        'user': UserProfileSerializer(user).data,
        'session_id': user_session.id
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        device_fingerprint = request.data.get('device_fingerprint', '')
        
        # Deactivate user session
        if device_fingerprint:
            UserSession.objects.filter(
                user=request.user,
                device_fingerprint=device_fingerprint
            ).update(is_active=False)
        else:
            # Logout from all devices
            UserSession.objects.filter(user=request.user).update(is_active=False)
        
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserSessionListView(generics.ListAPIView):
    """List user active sessions"""
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user, is_active=True)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def terminate_session(request, session_id):
    """Terminate a specific session"""
    try:
        session = UserSession.objects.get(
            id=session_id, 
            user=request.user, 
            is_active=True
        )
        session.is_active = False
        session.save()
        
        return Response({'message': 'Session terminated successfully'})
    except UserSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


class PasswordChangeView(generics.GenericAPIView):
    """Change user password"""
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Terminate all other sessions
        UserSession.objects.filter(user=user).update(is_active=False)
        
        return Response({'message': 'Password changed successfully'})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """API health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now(),
        'version': '1.0.0'
    })

from django.contrib.auth.models import User
from .models import Event
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken

class IsCreator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'CREATOR'

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'USER')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Utilisateur déjà existant'}, status=status.HTTP_409_CONFLICT)

    user = User.objects.create_user(username=username, email=email, password=password)

    user.profile.role = role
    user.profile.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    print(user)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        })
    return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_view(request):
    
    name = request.data.get('name')
    location = request.data.get('location')
    price = request.data.get('price')
    link = request.data.get('link')
    description = request.data.get('description')
    event_type = request.data.get('event_type')
    note = request.data.get('note')
    capacity = request.data.get('capacity')

    if not name or not location:
        return Response({'error': 'Le nom et le lieu sont obligatoires'}, status=status.HTTP_400_BAD_REQUEST)

    event = Event.objects.create(
        name=name,
        location=location,
        price=price or 0,
        link=link or '',
        description=description or '',
        event_type=event_type,
        note=note or 0,
        capacity=capacity or 0,
        creator=request.user
    )

    return Response({
        'message': 'Event créé',
        'event_id': event.id,
        'event_name': event.name
    }, status=status.HTTP_201_CREATED)

# --- EXEMPLE ROUTE SECURISEE ---
@api_view(['GET'])
@permission_classes([IsCreator])
def protected_view(request):
    return Response({'message': f'Bonjour {request.user.username}, tu es connecté !'})

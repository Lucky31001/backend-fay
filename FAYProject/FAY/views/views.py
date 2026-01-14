from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsCreator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'CREATOR'

# --- EXEMPLE ROUTE SECURISEE ---
@api_view(['GET'])
@permission_classes([IsCreator])
def protected_view(request):
    return Response({'message': f'Bonjour {request.user.username}, tu es connecté !'})

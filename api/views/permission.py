from rest_framework.permissions import BasePermission
from api.models import Agent

class IsProfileAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.agent.profile == Agent.PROFILE_ADMIN)
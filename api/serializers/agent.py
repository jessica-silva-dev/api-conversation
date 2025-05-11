from rest_framework import serializers
from api.models import Agent, TicketModel
from django.contrib.auth.models import User
from .ticket import TicketSerializer

class AgentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.username
    
    class Meta:
        model = Agent
        fields = [
            'id', 
            'user', 
            'username', 
            'profile', 
            'status'
        ]
        
class AgentTicketSerializer(serializers.ModelSerializer):
    
    ticket = TicketSerializer(read_only=True)
    
    username = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.username
    
    class Meta:
        model = Agent
        fields =[
            'id', 
            'user',
            'username',
            'profile', 
            'status', 
            'ticket',
        ]

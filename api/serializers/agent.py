from rest_framework import serializers
from api.models import Agent, TicketModel
from django.contrib.auth.models import User

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
    
    ticket = serializers.SerializerMethodField()
    
    def get_ticket(self, obj):
        from api.serializers.ticket import TicketSerializer
        if obj.ticket:
            return TicketSerializer(obj.ticket, read_only=True).data
    
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

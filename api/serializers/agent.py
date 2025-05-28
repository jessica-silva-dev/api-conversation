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
    
    tickets = serializers.SerializerMethodField()
    
    def get_tickets(self, obj):
        from api.serializers.ticket import TicketSerializer
        tickets = obj.tickets.all()
        return TicketSerializer(tickets, many=True, read_only=True).data
    
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
            'tickets',
        ]

from rest_framework import serializers
from api.models import TicketModel

class TicketSerializer(serializers.ModelSerializer):
    
    agent = serializers.SerializerMethodField()
    
    def get_agent(self, object):
        from api.serializers.agent import AgentSerializer
    
        if object.agent:
            return AgentSerializer(object.agent, read_only=True).data
        
    class Meta:
        model = TicketModel
        fields = ['id', 'status', 'created_at', 'agent']

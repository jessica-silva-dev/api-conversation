from rest_framework import serializers
from api.models import TicketModel

class TicketSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    
    def get_name(self, obj):
        return obj.contact.name
    
    class Meta:
        model = TicketModel
        fields = ['id', 'name', 'agent', 'status', 'created_at']

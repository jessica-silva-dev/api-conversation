from rest_framework import serializers
from api.models import Message
from .ticket import TicketSerializer

class MessageSerializer(serializers.ModelSerializer):
    identifier = serializers.SerializerMethodField()

    ticket = TicketSerializer(read_only=True)
    
    def get_identifier(self, object):
        return object.ticket.contact.identifier
    
    class Meta:
        model = Message
        fields = ['id', 'identifier', 'content', 'ticket']
        
from rest_framework import serializers
from api.models import Contact, Message
from api.serializers.message import MessageSerializer 

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        

class ContactMessageSerializer(serializers.ModelSerializer):
    
    '''
    messages = MessageSerializer(source='message_set', many=True, read_only=True)
    
    message_count = serializers.SerializerMethodField('get_message_count')
    
    def get_message_count(self, object):
        return Message.objects.filter(contact=object).count()
    
    '''
    
    messages = serializers.SerializerMethodField()
    
    def get_messages(self, object):
        messages = Message.objects.filter(ticket__contact__identifier= object.identifier)
        return MessageSerializer(messages, many=True).data
       
       #return MessageSerializer(Message.objects.filter(ticket__contact__identifier=object), many=True).data

    class Meta:
        model = Contact
        fields = ['messages']

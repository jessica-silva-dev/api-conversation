from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from api.serializers.message import MessageSerializer
from api.models import Message, TicketModel, Contact
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from api.util.validate_phonenumber import ValidatePhone
from matcher.views import TransferTicketAgent


class MessagesApiView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        messages = Message.objects.all().order_by('created_at')
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
class MessageCreateApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        content = request.data.get('content')
        content_type = request.data.get('content_type')
        identifier = request.data.get('identifier')
        name = request.data.get('name')
        user = request.data.get('user')
        
        if not all([content, content_type, identifier, name]):
            return Response({"error": "The fields content, content_type, identifier and is required"}, status.HTTP_400_BAD_REQUEST)
        
        try:
                    
            validate_identifier = ValidatePhone.validate_phone_number(identifier)
                
            if not validate_identifier:
                return Response({"error": "Invalid phone number"}, status.HTTP_400_BAD_REQUEST)
                
            contact, created = Contact.objects.get_or_create(
                identifier = validate_identifier,
                defaults={
                    "name": name
                }
            )
                
            agent = TransferTicketAgent()
            
            ticket = TicketModel.objects.create(
                contact = contact,
                agent = agent.assign_agent_ticket(),
                status = TicketModel.STATUS_OPEN,
                )
            
            message = Message.objects.create(
                ticket = ticket,
                content = content,
                content_type = content_type
            ) 
            
            serializer = MessageSerializer(message)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class MessageDetailApiView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
    
        ticket_id = kwargs.get('ticket')
        
        try:
            message = Message.objects.get(ticket__id=ticket_id)
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})


class ContactMessageApiView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        
        try:
            messages = Message.objects.filter(ticket__contact__identifier=identifier)
            if messages.exists():
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})
        
class MessageResetApiView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        ticket = kwargs.get('ticket')
        
        if not ticket:
            return Response({'error: Ticket is required'}, status.HTTP_400_BAD_REQUEST)
        
        try:
            message = Message.objects.get(ticket=ticket) 
            
            serializer = MessageSerializer(message, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK) 
        except Exception as e:
            return Response({'error': str(e)})
            
from rest_framework.permissions import IsAuthenticated
from api.util.validate_phonenumber import ValidatePhone
from api.serializers.contact import ContactSerializer, ContactMessageSerializer
from api.models import Contact, Message
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class ContactListMessegesApiView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, *args , **kwargs):
        identifier = kwargs.get('identifier')
        
        if not identifier:
            return Response({"message": "error identifier is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        contact = Contact.objects.get(identifier=identifier)
        
        if not contact:
            return Response({"message": "Contact not found"}, status.HTTP_404_NOT_FOUND)
        
        serializer = ContactMessageSerializer(contact)
        return Response(serializer.data, status.HTTP_200_OK)
        
class ContactApiView(APIView):
    
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        contact = Contact.objects.all()
        
        serializer = ContactSerializer(contact, many= True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        new_name = request.data.get('name')
        new_identifier = request.data.get('identifier')
        
        if not new_name:
            return Response({'error: name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not new_identifier:
            return Response({'error: Identifier is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Contact.objects.filter(identifier=new_identifier).exists():
            return Response({'error: Identifier exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            identifier = ValidatePhone.validate_phone_number(new_identifier)
            
            if  identifier is None:
                return Response({'error': 'Invalid phone number'}, status.HTTP_400_BAD_REQUEST)
                            
            if identifier:    
                new_contact = Contact.objects.create(
                    name=new_name,
                    identifier=identifier,
                )
                
                serializer = ContactSerializer(new_contact).data
                return Response(serializer, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ContactDetailApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        contact = Contact.objects.get(identifier=kwargs['identifier'])
        
        serializer = ContactSerializer(contact).data
        return Response(serializer, status=status.HTTP_200_OK)
    
    
class ContactResetdApi(APIView):
    #permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        
        identifier = kwargs.get('identifier')
        
        if not identifier:
            return Response({'error: Identifier is required'}, status.HTTP_400_BAD_REQUEST)
        try:
            contact = Contact.objects.get(identifier=identifier)
            
            serializer = ContactSerializer(contact, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "payload is not valid"})
        except Exception as e:
            return Response({'error': str(e)})
        
    
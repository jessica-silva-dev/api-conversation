from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers.agent import AgentSerializer, AgentTicketSerializer
from api.models import Agent, TicketModel

class AgentApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        profile = request.data.get('profile')
        
        if not all(['username', 'password']):
            return Response({'error': 'username is required'}, status.HTTP_400_BAD_REQUEST)
        
            return Response({'error': 'password is required'}, status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            return Response({'error': 'User exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_user = User.objects.create_user(
                username=username,
                password=password,
            )
            
            new_agent = Agent.objects.create(
                user=new_user,
                profile=profile,
                status=Agent.STATUS_ONLINE,
            )
            serializer = AgentSerializer(new_agent)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)})
        
class AgentDetailApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')        
        
        if not username:
            return Response({"message": "error username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            agent = Agent.objects.get(user__username=username)
            
            serializer = AgentSerializer(agent).data
            return Response(serializer, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AgentResetApiview(APIView):
    
    def patch(self, request, *args, **kwargs):
        
        username = kwargs.get('username')
        
        if not username:
            return Response({"message": "username is required"}, status.HTTP_404_NOT_FOUND)
                
        try:
            agent = Agent.objects.get(user__username= username)
            
            serializer = AgentSerializer(agent, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AgentListTicketApiView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        username = kwargs.get('username')
         
        if not username:
            return Response({"message": "error username is required"}, status.HTTP_400_BAD_REQUEST)
        
        try:
            tickets = TicketModel.objects.filter(agent__user__username=username)
            
            serializer = AgentTicketSerializer(tickets, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
            
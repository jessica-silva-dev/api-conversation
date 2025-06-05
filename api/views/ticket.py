from api.models import TicketModel, Agent
from rest_framework.views import APIView
from api.serializers.ticket import TicketSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.views.permission import IsProfileAdmin
from datetime import datetime, timedelta
from django.utils import timezone
from matcher.views import TransferTicketAgent

class TicketsOpenApiView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            agent = request.user.agent.get()
        except Agent.DoesNotExist:
            return Response({"message":  "Nenhum agente associado a este usuário."}, status.HTTP_400_BAD_REQUEST)
        
        try:
            if agent.profile == Agent.PROFILE_ADMIN:
                tickets = TicketModel.objects.filter(status=TicketModel.STATUS_OPEN)
            else:
                tickets = TicketModel.objects.filter(agent=agent, status=TicketModel.STATUS_OPEN)
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class TicketsCurrentDayApiView(APIView):
    permission_classes = [IsAuthenticated, IsProfileAdmin]
    
    def get(self, request, *args, **kwargs):
        
        agent = request.user.agent
        
        day = timezone.now()
        start_hour = day.replace(hour=0, minute=0, second=0)
        end_hour = day.replace(hour=23, minute=59, second=59)
        
        tickets = TicketModel.objects.filter(created_at__range=(start_hour, end_hour))

class AssignedTicketAgent(APIView):
    
    def patch(self, request, *args, **kwarags):
        
        try:
            TransferTicketAgent().transfer_agents_online()
            return Response({"message": "ok"},status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
            

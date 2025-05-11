from api.models import TicketModel, Agent
from rest_framework.views import APIView
from api.serializers.ticket import TicketSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.views.permission import IsProfileAdmin
from datetime import datetime, timedelta
from django.utils import timezone

class TicketsOpenApiView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        agent = request.user.agent
        
        if agent.profile == Agent.PROFILE_ADMIN:
            tickets = TicketModel.objects.filter(status=TicketModel.STATUS_OPEN)
        else:
            tickets = TicketModel.objects.filter(agent=agent, status=TicketModel.STATUS_OPEN)
        
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TicketsCurrentDayApiView(APIView):
    permission_classes = [IsAuthenticated, IsProfileAdmin]
    
    def get(self, request, *args, **kwargs):
        
        agent = request.user.agent
        
        day = timezone.now()
        start_hour = day.replace(hour=0, minute=0, second=0)
        end_hour = day.replace(hour=23, minute=59, second=59)
        
        tickets = TicketModel.objects.filter(created_at__range=(start_hour, end_hour))
    
    
    '''
    função: buscar todos os tickets do dia entre o horário de 00:00 até 23:59:59
    
    1° Pegar a data e a hora 
    2° fazer um filtro com o intervalo de horario entre 00:00 e 23:59 hrs
    
    '''    
    
    
    
    
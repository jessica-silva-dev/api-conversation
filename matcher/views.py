from api.models import Agent, TicketModel
from django.db.models import Count, Q

class TransferTicketAgent(): 
     
    def assign_agent_ticket(self):
        
        return Agent.objects.filter(profile= Agent.PROFILE_ATTENDANT, status= Agent.STATUS_ONLINE).annotate(
            count_agent_ticket=Count('tickets', filter=Q(tickets__status='Open'))
        ).order_by('count_agent_ticket').first()
        
                   
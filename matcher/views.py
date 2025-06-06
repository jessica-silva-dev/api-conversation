from api.models import Agent, TicketModel
from django.db.models import Count, Q
import time
from typing import List

class TransferTicketAgent(): 
    
    def transfer_agents_online(self):
        
        print("executando ...")
        
        tickets = TicketModel.objects.filter(agent__isnull=True, status='Open').order_by('created_at')

        if not tickets:
            return
        
        agents = self.get_agent_online()
        
        if not agents:
            return None
        
        for ticket in tickets:
            agent_more_free = self.get_agent_more_free(agents)
            agent_more_free.count_agent_ticket += 1
            ticket.agent = agent_more_free
            
        TicketModel.objects.bulk_update(tickets, ['agent'])
        
            
    def get_agent_more_free(self, agents):
        
        agent_min = None
        
        for agent in agents:
            
            if agent_min is None or agent.count_agent_ticket < agent_min.count_agent_ticket:
                agent_min = agent
        
        return agent_min
    
    def get_agent_online(self):
        
        return Agent.objects.filter(profile= Agent.PROFILE_ATTENDANT, status= Agent.STATUS_ONLINE).annotate(
            count_agent_ticket=Count('tickets', filter=Q(tickets__status='Open'))
        )
        
        
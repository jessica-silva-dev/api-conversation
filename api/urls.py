from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.contact import ContactListMessegesApiView, ContactApiView, ContactDetailApiView, ContactResetdApi
from api.views.message import  MessagesApiView, MessageCreateApiView, MessageDetailApiView, ContactMessageApiView, MessageResetApiView
from .views.agent import AgentApiView, AgentDetailApiView, AgentResetApiview, AgentListTicketApiView
from .views.ticket import TicketsOpenApiView, TicketsCurrentDayApiView

urlpatterns = [
    
    # Token
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    
    # Contact
    path('contacts/', ContactApiView.as_view()),
    path('contact/messages/<str:identifier>', ContactListMessegesApiView.as_view()),
    path('contact/detail/<str:identifier>', ContactDetailApiView.as_view()),
    path('contact/reset/<str:identifier>', ContactResetdApi.as_view()),
    
    # Message
    path('messages/', MessagesApiView.as_view()),
    path('message/create/', MessageCreateApiView.as_view()),
    path('message/list/<str:identifier>', ContactMessageApiView.as_view()),
    path('message/detail/<str:ticket>', MessageDetailApiView.as_view()),
    path('message/reset/<str:ticket>', MessageResetApiView.as_view()),
    
    #Agent
    path('agents/', AgentApiView.as_view()),
    path('agent/detail/<str:username>', AgentDetailApiView.as_view()),
    path('agent/reset/<str:username>', AgentResetApiview.as_view()),
    path('agent/tickets/<str:username>', AgentListTicketApiView.as_view()),
    
    #Ticket
    path('tickets/open/', TicketsOpenApiView.as_view()),
    path('tickets/open/day', TicketsCurrentDayApiView.as_view()),
   
]


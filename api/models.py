from django.db import models
from django.contrib.auth.models import User
import uuid

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30, db_index=True)
    identifier = models.CharField(max_length=13, unique=True, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
            
    def __str__(self):
        return self.name
    
class Agent(models.Model):
    PROFILE_ADMIN = 'administrator'
    PROFILE_ATTENDANT = 'attendant'
    
    PROFILE_CHOICES = [
        (PROFILE_ADMIN, 'administrator'),
        (PROFILE_ATTENDANT, 'attendant'),
    ]
    
    STATUS_ONLINE = 'Online'
    STATUS_OFFLINE = 'Offline'
    STATUS_PAUSE = 'Pause'
    
    STATUS_CHOICE = [
        (STATUS_ONLINE, 'Online'),
        (STATUS_OFFLINE, 'Offline'),
        (STATUS_PAUSE, 'Pause'),
    ]
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    profile = models.CharField(max_length=50, choices=PROFILE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE)
        
class TicketModel(models.Model):
    STATUS_OPEN = 'Open'
    STATUS_CLOSED = 'Closed'
    
    STATUS_CHOICE = [
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    agent = models.ForeignKey(to=Agent, on_delete=models.PROTECT, null=True, related_name='tickets')
    status = models.CharField(max_length=30, null=False, choices=STATUS_CHOICE, default='Open')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
                    
class Message(models.Model):
    CONTENT_TYPE_TEXT = 'Text'
    CONTENT_TYPE_DOCS = 'Docs'
    CONTENT_TYPE_MEDIA = 'Media'
    
    CONTENT_TYPE_CHOICE = [
        (CONTENT_TYPE_TEXT, 'Text'),
        (CONTENT_TYPE_DOCS, 'Docs'),
        (CONTENT_TYPE_MEDIA, 'Media'),
    ]
    
    ticket = models.ForeignKey(TicketModel, on_delete=models.PROTECT)
    content = models.TextField()
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPE_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    